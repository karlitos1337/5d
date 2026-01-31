import { describe, it, expect, vi } from 'vitest';
import { debounce } from '../modules/utils.js';

describe('debounce', () => {
  it('should delay execution', () => {
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

  it('should coalesce multiple calls', () => {
    vi.useFakeTimers();
    const func = vi.fn();
    const debouncedFunc = debounce(func, 100);

    debouncedFunc();
    vi.advanceTimersByTime(50);
    debouncedFunc();
    vi.advanceTimersByTime(50);
    expect(func).not.toHaveBeenCalled();

    vi.advanceTimersByTime(51);
    expect(func).toHaveBeenCalledTimes(1);

    vi.useRealTimers();
  });
});
