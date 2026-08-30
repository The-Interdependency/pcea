# ratios: loc_comments=37:8 imports_exports=6:1 calls_definitions=15:2
# GPT/Claude generated; context, prompt Erin Spencer
"""Compatibility imports for PCEA-UCNS proving-ground harnesses.

The current org workspace may expose recursive UCNS APIs as either
``ucns_recursive.*`` or as the legacy source tree under
``interdependent-lib/libs/ucns/src``. These helpers make that dependency
explicit and keep missing API errors visible to skip reasons.
"""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path
from types import ModuleType


def _install_legacy_ucns_recursive() -> bool:
    legacy_dir = Path(__file__).resolve().parents[2] / "interdependent-lib" / "libs" / "ucns" / "src"
    if not (legacy_dir / "canonical.py").exists():
        return False

    package = sys.modules.get("ucns_recursive")
    if package is None:
        package = types.ModuleType("ucns_recursive")
        package.__package__ = "ucns_recursive"
        package.__path__ = [str(legacy_dir)]  # type: ignore[attr-defined]
        sys.modules["ucns_recursive"] = package
    elif hasattr(package, "__path__"):
        paths = list(package.__path__)  # type: ignore[attr-defined]
        if str(legacy_dir) not in paths:
            paths.append(str(legacy_dir))
            package.__path__ = paths  # type: ignore[attr-defined]
    return True


def import_ucns_module(name: str) -> ModuleType:
    """Import a recursive UCNS module or raise an actionable ImportError."""
    tried: list[str] = []
    for prefix in ("ucns_recursive", "ucns"):
        module_name = f"{prefix}.{name}"
        try:
            return importlib.import_module(module_name)
        except ImportError as exc:
            tried.append(f"{module_name}: {exc}")

    if _install_legacy_ucns_recursive():
        module_name = f"ucns_recursive.{name}"
        try:
            return importlib.import_module(module_name)
        except ImportError as exc:
            tried.append(f"{module_name} via interdependent-lib legacy tree: {exc}")

    raise ImportError("recursive UCNS API unavailable; tried " + "; ".join(tried))
# ratios: loc_comments=37:8 imports_exports=6:1 calls_definitions=15:2
