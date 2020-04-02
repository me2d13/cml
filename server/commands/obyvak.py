from .abstract_command import CmlAbstractCommand, JALO_DOWN, JALO_STOP, JALO_UP, JaloCommand


def create_commands():
    return {
        "250": JaloCommand("250", "Zaluzie obyvak Z dolu", 1, JALO_DOWN),
        "251": JaloCommand("251", "Zaluzie obyvak Z nahoru", 1, JALO_UP),
        "252": JaloCommand("252", "Zaluzie obyvak Z stop", 1, JALO_STOP),
    }