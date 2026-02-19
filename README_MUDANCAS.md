# Documentação de mudanças e arquitetura (versão sem banco de dados)

## 1. Sem banco de dados
- Todas as filas e partidas são mantidas em memória (resetam ao reiniciar)
- Não há persistência, ranking ou histórico salvo

## 2. Estruturas em memória
- `utils/memory_store.py` mantém filas e partidas:
    - `queues = {guild_id: [user_id, ...]}`
    - `matches = {match_id: {team1: [...], team2: [...], status: 'waiting'}}`

## 3. Modularidade e handlers
- Estrutura modular: commands/, events/, handlers/, config/, utils/
- Handlers seguros para comandos, eventos, permissões e erros globais
- Logging centralizado (utils/logger.py)
- Uso correto de async/await, try/catch
- Separação clara entre lógica e configuração

## 4. Como usar
- Rode normalmente, sem dependências de banco
- Para adicionar comandos/eventos, basta criar arquivos em commands/ ou events/

## 5. Observação
- Se precisar de persistência futura (ranking, histórico), basta adicionar um banco de dados.

---

Se quiser exemplos de comandos, eventos ou integração com APIs externas, só pedir!
