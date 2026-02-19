# 🎮 Bot de Apostas Discord

## 📋 Visão Geral
Bot desenvolvido para gerenciar apostas em partidas de Free Fire através do Discord.

## ⚙️ Características Técnicas

### Armazenamento Volátil
Sistema opera com dados em RAM - informações são perdidas ao reiniciar o bot.

### Organização do Código
```
├── commands/     → Comandos do bot
├── events/       → Eventos Discord
├── handlers/     → Processadores de requisições
├── config/       → Configurações
├── utils/        → Ferramentas auxiliares
└── services/     → Lógica de negócio
```

### Recursos Implementados
- Sistema de filas para pareamento
- Criação automática de canais de partida
- Logs estruturados
- Tratamento de erros global
- Código assíncrono otimizado

## 🚀 Execução

1. Configure o `.env` com seu token
2. Instale dependências: `pip install -r requirements.txt`
3. Execute: `python main.py`

## 📝 Notas

- Dados não persistem entre reinicializações
- Extensível para adicionar banco de dados
- Pronto para novos comandos e eventos
