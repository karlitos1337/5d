import { describe, test, expect, vi } from 'vitest';
import { debounce } from '../modules/utils.js';

describe('Utils', () => {
  test('debounce delays execution', () => {
    vi.useFakeTimers();
    const func = vi.fn();
    const debouncedFunc = debounce(func, 100);

    debouncedFunc();
    expect(func).not.toHaveBeenCalled();

    vi.advanceTimersByTime(50);
    expect(func).not.toHaveBeenCalled();

    vi.advanceTimersByTime(51);
    expect(func).toHaveBeenCalledTimes(1);

    vi.useRealTimers();
  });

  test('debounce groups multiple calls', () => {
    vi.useFakeTimers();
    const func = vi.fn();
    const debouncedFunc = debounce(func, 100);

    debouncedFunc();
    vi.advanceTimersByTime(50);
    debouncedFunc();
    vi.advanceTimersByTime(50);
    debouncedFunc();

    expect(func).not.toHaveBeenCalled();

    vi.advanceTimersByTime(101);
    expect(func).toHaveBeenCalledTimes(1);

    vi.useRealTimers();
  });
});
