"""Identificador de bandeira de cartão de crédito.

Este módulo fornece funções para:
- limpar um número de cartão
- verificar o dígito verificador pelo algoritmo de Luhn
- identificar a bandeira (Visa, MasterCard, American Express, Discover, etc.)

Saída: para cada número informado, mostra a bandeira detectada e se o
cartão passa na verificação Luhn.

Uso:
  python identificador_bandeira_cartao.py 4111111111111111 378282246310005

Se executado sem argumentos, entra em modo interativo (prompt).
"""
from __future__ import annotations

import argparse
import re
from typing import Optional, Tuple


def _clean(number: str) -> str:
    """Remove tudo que não for dígito."""
    return re.sub(r"\D", "", number or "")


def luhn_check(number: str) -> bool:
    """Retorna True se o número passar no algoritmo de Luhn.

    O número deve ser apenas dígitos.
    """
    n = _clean(number)
    if not n:
        return False
    total = 0
    reverse_digits = n[::-1]
    for i, d in enumerate(reverse_digits):
        digit = int(d)
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def detect_brand(number: str) -> Optional[str]:
    """Detecta a bandeira a partir do número limpo (apenas dígitos).

    Retorna o nome da bandeira ou None se não for possível identificar.
    """
    n = _clean(number)
    ln = len(n)
    if not n:
        return None

    # Visa
    if n.startswith("4") and ln in (13, 16, 19):
        return "Visa"

    # MasterCard (51-55) e (2221-2720)
    if ln == 16:
        try:
            first2 = int(n[:2])
            first4 = int(n[:4])
        except ValueError:
            first2 = first4 = -1
        if 51 <= first2 <= 55 or 2221 <= first4 <= 2720:
            return "MasterCard"

    # American Express
    if ln == 15 and n.startswith(("34", "37")):
        return "American Express"

    # Discover (6011, 622126-622925, 644-649, 65)
    if ln in (16, 19):
        if n.startswith("6011") or n.startswith("65") or (len(n) >= 3 and 644 <= int(n[:3]) <= 649):
            return "Discover"
        if len(n) >= 6 and 622126 <= int(n[:6]) <= 622925:
            return "Discover"

    # JCB (3528-3589)
    if 16 <= ln <= 19 and len(n) >= 4 and 3528 <= int(n[:4]) <= 3589:
        return "JCB"

    # Diners Club (300-305, 36, 38, 39)
    if ln == 14 and (n.startswith("36") or (len(n) >= 3 and 300 <= int(n[:3]) <= 305)):
        return "Diners Club"

    # Elo - usa muitos BINs; aqui verificamos alguns prefixos comuns.
    elo_prefixes = ("4011", "4312", "4389", "4514", "4576", "5067", "506699", "5090", "6277", "6362", "6363", "5041")
    if any(n.startswith(p) for p in elo_prefixes):
        return "Elo"

    # Hipercard (prefixos variados; heurística simples)
    if ln >= 13 and (n.startswith("38") or n.startswith("60")):
        return "Hipercard"

    return None


def format_result(number: str) -> Tuple[str, str, bool]:
    """Retorna (clean_number, brand_or_msg, luhn_ok)."""
    clean = _clean(number)
    brand = detect_brand(clean) or "Bandeira não identificada"
    luhn_ok = luhn_check(clean)
    return clean, brand, luhn_ok


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Identificador de bandeira de cartão + verificação Luhn")
    p.add_argument("numbers", nargs="*", help="Números de cartão a analisar (pode conter espaços ou hífens). Se vazio, entra em modo interativo.")
    return p.parse_args()


def main():
    args = _parse_args()
    if not args.numbers:
        # Modo interativo
        print("--- Identificador de Bandeira de Cartão de Crédito ---")
        print("Pressione Enter em vazio para sair.")
        while True:
            try:
                s = input("Número do cartão: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not s:
                break
            clean, brand, ok = format_result(s)
            print(f"{clean} -> {brand} | Luhn: {'válido' if ok else 'inválido'}")
    else:
        for s in args.numbers:
            clean, brand, ok = format_result(s)
            print(f"{clean} -> {brand} | Luhn: {'válido' if ok else 'inválido'}")


if __name__ == "__main__":
    main()