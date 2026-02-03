import { describe, it, expect, vi } from 'vitest';
import { debounce } from '../modules/utils.js';

describe('debounce', () => {
  it('should debounce function calls', () => {
    vi.useFakeTimers();
    const func = vi.fn();
    const debouncedFunc = debounce(func, 100);

    debouncedFunc();
    debouncedFunc();
    debouncedFunc();

    expect(func).not.toHaveBeenCalled();

    vi.advanceTimersByTime(100);

    expect(func).toHaveBeenCalledTimes(1);
    vi.useRealTimers();
  });

  it('should execute with correct arguments', () => {
    vi.useFakeTimers();
    const func = vi.fn();
    const debouncedFunc = debounce(func, 100);

    debouncedFunc('test');
    vi.advanceTimersByTime(100);

    expect(func).toHaveBeenCalledWith('test');
    vi.useRealTimers();
  });
});
