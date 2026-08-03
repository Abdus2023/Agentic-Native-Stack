/**
 * Source: agentic-native-stack.md
 * Context: QX.3 Locale Detection
 * Extraction ID: CODE-112
 * Knowledge Links: KI-172
 * Status: scaffolded
 */

export interface LocaleContext {
  locale: string;
  timezone: string;
  numberingSystem: string;
  calendar: string;
  textDirection: "ltr" | "rtl";
}

export function detectLocale(): LocaleContext {
  const locale = navigator.language ?? "en-US";
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const direction = new Intl.Locale(locale).textInfo?.direction ?? "ltr";

  return {
    locale,
    timezone,
    numberingSystem: "latn",
    calendar: "gregory",
    textDirection: direction as "ltr" | "rtl",
  };
}

export function formatTimestamp(ms: number, locale: LocaleContext): string {
  return new Intl.DateTimeFormat(locale.locale, {
    dateStyle: "medium",
    timeStyle: "long",
    timeZone: locale.timezone,
  }).format(new Date(ms));
}

export function formatNumber(value: number, locale: LocaleContext): string {
  return new Intl.NumberFormat(locale.locale, {
    numberingSystem: locale.numberingSystem,
  }).format(value);
}

export function formatBytes(bytes: number, locale: LocaleContext): string {
  const units = ["B", "KB", "MB", "GB", "TB"];
  let value = bytes;
  let unit = 0;

  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }

  return `${formatNumber(Math.round(value * 10) / 10, locale)} ${units[unit]}`;
}