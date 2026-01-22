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

  it('should reset timer on subsequent calls', () => {
    vi.useFakeTimers();
    const func = vi.fn();
    const debouncedFunc = debounce(func, 100);

    debouncedFunc();
    vi.advanceTimersByTime(50);
    debouncedFunc(); // reset timer

    vi.advanceTimersByTime(50);
    expect(func).not.toHaveBeenCalled(); // 100ms total, but reset at 50ms

    vi.advanceTimersByTime(51);
    expect(func).toHaveBeenCalledTimes(1);
    vi.useRealTimers();
  });

  it('should pass arguments correctly', () => {
    vi.useFakeTimers();
    const func = vi.fn();
    const debouncedFunc = debounce(func, 100);

    debouncedFunc('hello', 42);
    vi.advanceTimersByTime(101);

    expect(func).toHaveBeenCalledWith('hello', 42);
    vi.useRealTimers();
  });
});
