# Documentação de mudanças e arquitetura

## 1. Pool de Conexões (SQLite)
- Implementado em utils/db_pool.py
- Todas as operações de banco usam get_conn()/release_conn() para evitar travamentos e garantir performance mesmo com muitos usuários.

## 2. Pareamento até 4v4
- O banco matches agora armazena team1 e team2 como JSON (listas de user_ids).
- O bot busca até 8 jogadores na fila, divide em dois times (2v2, 3v3, 4v4) e cria o canal para todos.
- Permissões e embed são configurados para todos os jogadores dos dois times.
- Confirmação de aposta é individual: só avança quando todos confirmam.

## 3. Download de avatar
- O bot só baixa o avatar se não existir localmente, evitando lentidão e requisições desnecessárias.

## 4. Banner e bio
- Removida qualquer tentativa de alterar banner/bio via bot, pois não é permitido pela API do Discord.

## 5. Segurança e arquitetura
- Estrutura modular: commands/, events/, handlers/, config/, utils/
- Handlers seguros para comandos, eventos, permissões e erros globais
- Logging centralizado (utils/logger.py)
- Uso correto de async/await, try/catch
- Separação clara entre lógica e configuração

## 6. Pronto para produção
- O bot está seguro, escalável, fácil de manter e pronto para features avançadas.
- Para adicionar comandos/eventos, basta criar arquivos em commands/ ou events/.

---
