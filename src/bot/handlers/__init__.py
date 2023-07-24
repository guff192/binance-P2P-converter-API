from .start_help_handlers import register_start_help_handlers


def register_message_handlers(bot):
    register_start_help_handlers(bot)

