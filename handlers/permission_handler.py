# handlers/permission_handler.py
"""
Validação automática de permissões para comandos.
"""
from discord.ext import commands
from utils.logger import log_warning

async def check_permissions(ctx, required_perms=None):
    if required_perms is None:
        return True
    perms = ctx.author.guild_permissions
    for perm in required_perms:
        if not getattr(perms, perm, False):
            log_warning(f"Permissão negada: {perm} para {ctx.author}")
            return False
    return True
