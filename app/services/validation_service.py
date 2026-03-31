import re

PROFANITY_LIST = [
    # Português
    "merda", "porra", "foda", "fode", "fodase", "foda-se", "caralho", "puta",
    "putaria", "viado", "viadinho", "cu", "buceta", "pau", "piroca", "cacete",
    "arrombado", "babaca", "idiota", "imbecil", "retardado", "cuzão", "filha da puta",
    "filho da puta", "fdp", "vsf", "vai se foder", "vai tomar no cu", "corno",
    "desgraça", "desgraçado", "lixo", "vagabundo", "vagabunda", "prostituta",
    "putinha", "safado", "safada", "otário", "otaria", "abestado",
    # English
    "fuck", "shit", "ass", "asshole", "bitch", "bastard", "damn", "crap",
    "dick", "cock", "pussy", "cunt", "motherfucker", "mf", "wtf", "stfu",
    "idiot", "moron", "stupid",
]

IT_KEYWORDS = [
    # Problemas de hardware
    "computador", "computer", "pc", "notebook", "laptop", "monitor", "teclado",
    "mouse", "impressora", "printer", "scanner", "servidor", "server",
    "reiniciando", "reiniciar", "desligando", "travando", "travado", "lento",
    "não liga", "nao liga", "não abre", "nao abre", "quebrou", "queimou",
    "tela azul", "blue screen", "bsod", "superaquecendo", "barulho",
    # Problemas de software
    "sistema", "system", "software", "programa", "aplicativo", "app",
    "windows", "linux", "macos", "office", "word", "excel", "outlook",
    "instalação", "instalacao", "instalar", "desinstalar", "atualização",
    "atualizacao", "atualizar", "update", "erro", "error", "travou",
    "não funciona", "nao funciona", "parou de funcionar", "crash",
    # Acesso e autenticação
    "senha", "password", "login", "acesso", "access", "bloqueado", "blocked",
    "conta", "account", "usuário", "usuario", "user", "perfil", "profile",
    "autenticação", "autenticacao", "authentication", "2fa", "mfa",
    "esqueci", "esqueceu", "redefinir", "reset", "expirou", "expirada",
    "credencial", "credential", "vpn", "remote", "remoto", "rdp",
    # Rede e conectividade
    "internet", "rede", "network", "wifi", "wi-fi", "cabo", "conexão",
    "conexao", "connection", "sem acesso", "sem internet", "lentidão",
    "lentidao", "slow", "roteador", "router", "switch", "firewall",
    "proxy", "dns", "ip", "vpn", "ping", "latência", "latencia",
    # Segurança
    "virus", "vírus", "malware", "ransomware", "spyware", "phishing",
    "hack", "hacker", "invadido", "invasão", "invasao", "suspeito",
    "antivirus", "antivírus", "infectado", "infecção", "infeccao",
    "ataque", "attack", "vulnerabilidade", "vulnerability", "brecha",
    # Email e comunicação
    "email", "e-mail", "correio", "mail", "caixa", "inbox", "spam",
    "outlook", "teams", "skype", "zoom", "meet", "mensagem", "message",
    "anexo", "attachment", "calendario", "calendar",
    # Arquivos e dados
    "arquivo", "file", "pasta", "folder", "documento", "document",
    "backup", "restaurar", "restore", "perdeu", "sumiu", "deletou",
    "excluiu", "apagou", "recuperar", "recovery", "dados", "data",
    "disco", "disk", "hd", "ssd", "armazenamento", "storage", "espaço",
    # Periféricos e dispositivos
    "celular", "telefone", "phone", "tablet", "headset", "fone",
    "webcam", "camera", "microfone", "microfono", "microphone",
    "pendrive", "usb", "hd externo", "nobreak", "ups",
    # Suporte e processos TI
    "ticket", "chamado", "solicitação", "solicitacao", "suporte", "support",
    "help desk", "helpdesk", "ti", "it", "técnico", "tecnico", "manutenção",
    "manutencao", "maintenance", "incidente", "incident", "problema", "problem",
    "instalação", "instalacao", "configuração", "configuracao", "configuration",
    "permissão", "permissao", "permission", "licença", "licenca", "license",
    "deploy", "implantação", "implantacao", "migração", "migracao",
]


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[àáâãä]", "a", text)
    text = re.sub(r"[èéêë]", "e", text)
    text = re.sub(r"[ìíîï]", "i", text)
    text = re.sub(r"[òóôõö]", "o", text)
    text = re.sub(r"[ùúûü]", "u", text)
    text = re.sub(r"[ç]", "c", text)
    return text


def _contains_profanity(text: str) -> bool:
    normalized = _normalize(text)
    words = re.split(r"[\s\W]+", normalized)
    word_set = set(words)
    for bad_word in PROFANITY_LIST:
        normalized_bad = _normalize(bad_word)
        if normalized_bad in word_set:
            return True
        if " " not in bad_word and normalized_bad in normalized:
            if re.search(r"\b" + re.escape(normalized_bad) + r"\b", normalized):
                return True
    return False


def _is_it_related(title: str, description: str) -> bool:
    combined = _normalize(f"{title} {description}")
    for keyword in IT_KEYWORDS:
        normalized_kw = _normalize(keyword)
        if normalized_kw in combined:
            return True
    return False


def validate_ticket(title: str, description: str) -> dict:
    """
    Returns {"valid": True} or {"valid": False, "error": "mensagem"}
    """
    if not title or not title.strip():
        return {"valid": False, "error": "O título do ticket é obrigatório."}

    if not description or not description.strip():
        return {"valid": False, "error": "A descrição do ticket é obrigatória."}

    if len(title.strip()) < 5:
        return {"valid": False, "error": "O título deve ter pelo menos 5 caracteres."}

    if len(description.strip()) < 15:
        return {"valid": False, "error": "A descrição deve ter pelo menos 15 caracteres."}

    full_text = f"{title} {description}"
    if _contains_profanity(full_text):
        return {
            "valid": False,
            "error": "Linguagem inadequada detectada. Por favor, descreva o problema de forma profissional."
        }

    if not _is_it_related(title, description):
        return {
            "valid": False,
            "error": (
                "O ticket não parece estar relacionado a suporte de TI. "
                "Por favor, descreva um problema técnico como: falha de acesso, "
                "erro de sistema, problema com senha, equipamento com defeito, etc."
            )
        }

    return {"valid": True}
