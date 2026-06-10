"""
TZ bo'lim 5 — Claude multi-prompt signal tahlili.

Zanjir:
  1. Haiku pre-screen  → zaif signal → WAIT (token tejash)
  2. Sonnet prompt 1   → texnik tahlil   (kesh bilan)
  3. Sonnet prompt 2   → makro/on-chain  (kesh bilan)
  4. Sonnet prompt 3   → risk/devil      (kesh bilan)
  5. Sonnet reflection → o'z-o'zini tanqid
  6. Sonnet aggregator → yakuniy qaror + ball
"""
import json
from dataclasses import dataclass
from typing import Any

from app.core.logger import logger
from app.services.ai.claude_client import get_client
from app.core.config import settings

# ---------------------------------------------------------------
# Keshlanadigan tizim prompti — barcha so'rovlarda bir xil
# ---------------------------------------------------------------
_SYSTEM_CACHED = """
Sen professional crypto trading AI assistantisan.
Har tahlilda quyidagi formatda javob ber (JSON):
{
  "direction": "LONG" | "SHORT" | "HOLD" | "WAIT",
  "confidence": 0.0-1.0,
  "reasoning": "qisqa asoslash (O'zbek tilida)",
  "key_levels": {"support": float, "resistance": float}
}
Faqat JSON qaytargın. Ko'proq matn yozma.
""".strip()


@dataclass
class AnalysisResult:
    direction: str          # LONG | SHORT | HOLD | WAIT
    confidence: float       # 0.0 – 1.0
    reasoning: str
    score: int              # 0 – 100
    signal_quality: str     # A+ | A | B | C | D
    details: dict[str, Any]


def _compress_ohlcv(candles: list[dict]) -> str:
    """OHLCV → CSV satr (token tejash TZ 5.4)."""
    rows = []
    for c in candles[-50:]:  # oxirgi 50 ta yetarli
        rows.append(f"{c['t']},{float(c['o']):.2f},{float(c['h']):.2f},{float(c['l']):.2f},{float(c['c']):.2f},{float(c['v']):.2f}")
    return "t,o,h,l,c,v\n" + "\n".join(rows)


def _parse_json_safe(text: str) -> dict:
    """JSON ni xavfsiz parse qilish."""
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except Exception:
        pass
    return {"direction": "WAIT", "confidence": 0.0, "reasoning": "parse xatosi", "key_levels": {}}


def _score_from_results(results: list[dict]) -> tuple[int, str]:
    """
    3 ta tahlil natijasidan signal ball va sifat hisoblash.
    TZ jadval 8.2: 85-100=A+, 70-84=A, 55-69=B, 40-54=C, <40=D
    """
    if not results:
        return 0, "D"

    # Har tahlilchi ovozi: direction × confidence
    direction_votes: dict[str, float] = {}
    for r in results:
        d = r.get("direction", "WAIT")
        c = float(r.get("confidence", 0.0))
        direction_votes[d] = direction_votes.get(d, 0.0) + c

    best_dir = max(direction_votes, key=lambda k: direction_votes[k])
    total_weight = sum(direction_votes.values())
    consensus = direction_votes.get(best_dir, 0.0) / max(total_weight, 0.001)

    # Ball: konsensus × 100, risk agent veto hisobga olinmagan (aggregator qiladi)
    score = int(consensus * 100)
    score = max(0, min(100, score))

    if score >= 85:
        quality = "A+"
    elif score >= 70:
        quality = "A"
    elif score >= 55:
        quality = "B"
    elif score >= 40:
        quality = "C"
    else:
        quality = "D"

    return score, quality


async def analyze_signal(
    symbol: str,
    candles: list[dict],
    current_price: float,
    timeframe: str = "1h",
) -> AnalysisResult:
    """
    To'liq 5-qadam tahlil zanjiri.
    candles: OHLCV lug'at ro'yxati
    """
    client = get_client()

    ohlcv_csv = _compress_ohlcv(candles)
    market_ctx = f"Symbol: {symbol} | Narx: {current_price:.4f} | TF: {timeframe}"

    # ---------------------------------------------------------------
    # Qadam 1 — Haiku pre-screen (token tejash)
    # ---------------------------------------------------------------
    pre_prompt = (
        f"{market_ctx}\n"
        f"Oxirgi 10 sham (c,v): "
        + ", ".join(f"{float(c['c']):.2f}/{float(c['v']):.0f}" for c in candles[-10:])
        + "\nBu signal kuchli ko'rinadi? Faqat 'HA' yoki 'YO'Q' de."
    )
    pre_response = client.messages.create(
        model=settings.ANTHROPIC_MODEL_HAIKU,
        max_tokens=10,
        messages=[{"role": "user", "content": pre_prompt}],
    )
    pre_text = pre_response.content[0].text.strip().upper() if pre_response.content else "YO'Q"
    logger.debug(f"Haiku pre-screen [{symbol}]: {pre_text}")

    if "HA" not in pre_text:
        logger.info(f"Pre-screen o'tkazilmadi [{symbol}] — WAIT qaytarildi")
        return AnalysisResult(
            direction="WAIT", confidence=0.0,
            reasoning="Haiku pre-screen: signal kuchsiz",
            score=0, signal_quality="D", details={"pre_screen": "failed"},
        )

    # Keshlanadigan tizim bloki — barcha 3 ta Sonnet so'rovida bir xil
    system_blocks = [
        {
            "type": "text",
            "text": _SYSTEM_CACHED,
            "cache_control": {"type": "ephemeral"},
        }
    ]

    # ---------------------------------------------------------------
    # Qadam 2 — Texnik tahlilchi (Sonnet)
    # ---------------------------------------------------------------
    tech_prompt = (
        f"{market_ctx}\n"
        f"OHLCV (oxirgi 50 sham):\n{ohlcv_csv}\n\n"
        "Texnik tahlil: trend, support/resistance, momentum."
    )
    tech_resp = client.messages.create(
        model=settings.ANTHROPIC_MODEL_SONNET,
        max_tokens=512,
        system=system_blocks,
        messages=[{"role": "user", "content": tech_prompt}],
    )
    tech_text = tech_resp.content[-1].text if tech_resp.content else "{}"
    tech_result = _parse_json_safe(tech_text)

    # ---------------------------------------------------------------
    # Qadam 3 — Makro/risk tahlilchi (Sonnet, kesh o'qiydi)
    # ---------------------------------------------------------------
    macro_prompt = (
        f"{market_ctx}\n"
        "Makro va risk tahlil: bozor rejimi, volatilitet, qarshi dalillar."
    )
    macro_resp = client.messages.create(
        model=settings.ANTHROPIC_MODEL_SONNET,
        max_tokens=512,
        system=system_blocks,
        messages=[{"role": "user", "content": macro_prompt}],
    )
    macro_text = macro_resp.content[-1].text if macro_resp.content else "{}"
    macro_result = _parse_json_safe(macro_text)

    # ---------------------------------------------------------------
    # Qadam 4 — Reflection (o'z-o'zini tanqid, TZ 5.2)
    # ---------------------------------------------------------------
    reflection_prompt = (
        f"Ushbu 2 ta tahlilni ko'rib chiqdim:\n"
        f"Texnik: {tech_text[:300]}\n"
        f"Makro: {macro_text[:300]}\n\n"
        "Eng kuchli qarshi dalil nima? Shunga qaramay yakuniy qarorim:"
    )
    reflect_resp = client.messages.create(
        model=settings.ANTHROPIC_MODEL_SONNET,
        max_tokens=512,
        system=system_blocks,
        messages=[{"role": "user", "content": reflection_prompt}],
    )
    reflect_text = reflect_resp.content[-1].text if reflect_resp.content else "{}"
    reflect_result = _parse_json_safe(reflect_text)

    # ---------------------------------------------------------------
    # Qadam 5 — Aggregator (yakuniy qaror)
    # ---------------------------------------------------------------
    all_analyses = [tech_result, macro_result, reflect_result]
    agg_prompt = (
        f"{market_ctx}\n"
        f"3 ta tahlilchi natijalari:\n"
        f"1. Texnik: dir={tech_result.get('direction')} conf={tech_result.get('confidence')}\n"
        f"2. Makro: dir={macro_result.get('direction')} conf={macro_result.get('confidence')}\n"
        f"3. Reflection: dir={reflect_result.get('direction')} conf={reflect_result.get('confidence')}\n\n"
        "Yakuniy qaror (TZ aggregatsiya protokoli asosida):"
    )
    agg_resp = client.messages.create(
        model=settings.ANTHROPIC_MODEL_SONNET,
        max_tokens=512,
        system=system_blocks,
        messages=[{"role": "user", "content": agg_prompt}],
    )
    agg_text = agg_resp.content[-1].text if agg_resp.content else "{}"
    agg_result = _parse_json_safe(agg_text)

    # ---------------------------------------------------------------
    # Natija hisoblash
    # ---------------------------------------------------------------
    score, quality = _score_from_results([agg_result, tech_result, macro_result])

    # Prompt kesh statistikasi log qilish
    usage = agg_resp.usage
    logger.info(
        f"Claude tahlil [{symbol}] | "
        f"Kesh_o'qildi={usage.cache_read_input_tokens} | "
        f"Kesh_yozildi={usage.cache_creation_input_tokens} | "
        f"Natija={agg_result.get('direction')} {score}/100"
    )

    return AnalysisResult(
        direction=agg_result.get("direction", "WAIT"),
        confidence=float(agg_result.get("confidence", 0.0)),
        reasoning=agg_result.get("reasoning", ""),
        score=score,
        signal_quality=quality,
        details={
            "technical": tech_result,
            "macro": macro_result,
            "reflection": reflect_result,
            "aggregated": agg_result,
            "cache_read_tokens": usage.cache_read_input_tokens,
        },
    )
