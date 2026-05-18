#!/usr/bin/env python3
"""
E-commerce REST API
Framework: Flask
Database: PostgreSQL
WSGI Server: Gunicorn
"""

from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
import os
from datetime import datetime
import socket
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Criar aplicação Flask
app = Flask(__name__)

# Configurações do banco de dados (sem hardcode de senha)
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'database': os.environ.get('DB_NAME', 'ecommerce'),
    'user': os.environ.get('DB_USER', 'appuser'),
    'password': os.environ['DB_PASSWORD']  # obrigatório
}

# Pool de conexões
connection_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)

def get_db_connection():
    return connection_pool.getconn()

def release_db_connection(conn):
    connection_pool.putconn(conn)

def get_server_info():
    return {
        'server': socket.gethostname(),
        'timestamp': datetime.now().isoformat()
    }

# ============================================
# ROTAS DA API
# ============================================

@app.route('/', methods=['GET'])
def health_check():
    """
    Health check - usado pelo Load Balancer
    
    O Load Balancer faz HTTP GET nesta rota a cada 15 segundos.
    Se retornar 200 OK, considera a VM "healthy".
    Se falhar 2x consecutivas, remove a VM do pool.
    """
    return jsonify({
        'status': 'ok',
        'message': 'E-commerce API funcionando!',
        **get_server_info()
    })

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    """
    GET /api/produtos
    
    Lista todos os produtos do banco de dados.
    Retorna JSON com array de produtos.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Query SQL
        cursor.execute('SELECT * FROM produtos ORDER BY id')
        produtos = cursor.fetchall()
        
        cursor.close()
        
        return jsonify({
            'total': len(produtos),
            'produtos': produtos,
            **get_server_info()
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao buscar produtos',
            'details': str(e)
        }), 500
        
    finally:
        if conn:
            release_db_connection(conn)

@app.route('/api/produtos/<int:produto_id>', methods=['GET'])
def buscar_produto(produto_id):
    """
    GET /api/produtos/:id
    
    Busca um produto específico por ID.
    Retorna 404 se não encontrado.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('SELECT * FROM produtos WHERE id = %s', (produto_id,))
        produto = cursor.fetchone()
        
        cursor.close()
        
        if not produto:
            return jsonify({
                'error': 'Produto não encontrado'
            }), 404
        
        return jsonify({
            'produto': produto,
            **get_server_info()
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao buscar produto',
            'details': str(e)
        }), 500
        
    finally:
        if conn:
            release_db_connection(conn)

@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    """
    POST /api/produtos
    Body: {"nome": "...", "preco": 99.90, "estoque": 10}
    
    Cria um novo produto no banco de dados.
    Retorna 201 Created com o produto criado.
    """
    conn = None
    try:
        # Validar dados recebidos
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Nenhum dado fornecido'
            }), 400
        
        nome = data.get('nome')
        preco = data.get('preco')
        estoque = data.get('estoque')
        
        if not nome or preco is None or estoque is None:
            return jsonify({
                'error': 'Campos obrigatórios: nome, preco, estoque'
            }), 400
        
        # Inserir no banco
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(
            'INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s) RETURNING *',
            (nome, preco, estoque)
        )
        
        produto = cursor.fetchone()
        conn.commit()  # Confirmar transação
        cursor.close()
        
        return jsonify({
            'message': 'Produto criado com sucesso',
            'produto': produto,
            **get_server_info()
        }), 201
        
    except Exception as e:
        if conn:
            conn.rollback()  # Reverter transação em caso de erro
        return jsonify({
            'error': 'Erro ao criar produto',
            'details': str(e)
        }), 500
        
    finally:
        if conn:
            release_db_connection(conn)

@app.route('/api/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    """
    PUT /api/produtos/:id
    Body: {"nome": "...", "preco": 199.90, "estoque": 20}
    
    Atualiza um produto existente.
    Campos não fornecidos não são alterados.
    """
    conn = None
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Nenhum dado fornecido'
            }), 400
        
        nome = data.get('nome')
        preco = data.get('preco')
        estoque = data.get('estoque')
        
        # Montar query dinamicamente (atualiza apenas campos fornecidos)
        updates = []
        params = []
        
        if nome is not None:
            updates.append('nome = %s')
            params.append(nome)
        
        if preco is not None:
            updates.append('preco = %s')
            params.append(preco)
        
        if estoque is not None:
            updates.append('estoque = %s')
            params.append(estoque)
        
        if not updates:
            return jsonify({
                'error': 'Nenhum campo para atualizar'
            }), 400
        
        params.append(produto_id)
        
        query = f"UPDATE produtos SET {', '.join(updates)} WHERE id = %s RETURNING *"
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(query, params)
        produto = cursor.fetchone()
        
        if not produto:
            cursor.close()
            return jsonify({
                'error': 'Produto não encontrado'
            }), 404
        
        conn.commit()
        cursor.close()
        
        return jsonify({
            'message': 'Produto atualizado com sucesso',
            'produto': produto,
            **get_server_info()
        })
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({
            'error': 'Erro ao atualizar produto',
            'details': str(e)
        }), 500
        
    finally:
        if conn:
            release_db_connection(conn)

@app.route('/api/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    """
    DELETE /api/produtos/:id
    
    Deleta um produto do banco de dados.
    Retorna 404 se não encontrado.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('DELETE FROM produtos WHERE id = %s RETURNING *', (produto_id,))
        produto = cursor.fetchone()
        
        if not produto:
            cursor.close()
            return jsonify({
                'error': 'Produto não encontrado'
            }), 404
        
        conn.commit()
        cursor.close()
        
        return jsonify({
            'message': 'Produto deletado com sucesso',
            'produto': produto,
            **get_server_info()
        })
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({
            'error': 'Erro ao deletar produto',
            'details': str(e)
        }), 500
        
    finally:
        if conn:
            release_db_connection(conn)

# ============================================
# TRATAMENTO DE ERROS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Rota não encontrada"""
    return jsonify({
        'error': 'Rota não encontrada'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Erro interno do servidor"""
    return jsonify({
        'error': 'Erro interno do servidor'
    }), 500

# ============================================
# INICIALIZAÇÃO
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 E-commerce API - Flask")
    print("=" * 50)
    print(f"Servidor: {socket.gethostname()}")
    print(f"Porta: {os.getenv('PORT', 3000)}")
    print(f"Database: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    print()
    print("Endpoints disponíveis:")
    print("  GET    /                    - Health check")
    print("  GET    /api/produtos        - Listar produtos")
    print("  GET    /api/produtos/:id    - Buscar produto")
    print("  POST   /api/produtos        - Criar produto")
    print("  PUT    /api/produtos/:id    - Atualizar produto")
    print("  DELETE /api/produtos/:id    - Deletar produto")
    print("=" * 50)
    print()
    
    # Rodar servidor
    # Em produção, isso não é usado (Gunicorn assume)
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
