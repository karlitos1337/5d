import { describe, test, expect, vi } from 'vitest';
import { debounce } from '../modules/utils.js';

describe('Utility Functions', () => {
  test('debounce delays execution', async () => {
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

  test('debounce calls only once for multiple calls within wait time', () => {
    vi.useFakeTimers();
    const func = vi.fn();
    const debouncedFunc = debounce(func, 100);

    debouncedFunc();
    debouncedFunc();
    debouncedFunc();

    vi.advanceTimersByTime(101);
    expect(func).toHaveBeenCalledTimes(1);
    vi.useRealTimers();
  });

  test('debounce passes arguments correctly', () => {
     vi.useFakeTimers();
     const func = vi.fn();
     const debouncedFunc = debounce(func, 100);

     debouncedFunc('hello', 123);
     vi.advanceTimersByTime(101);
     expect(func).toHaveBeenCalledWith('hello', 123);
     vi.useRealTimers();
  });
});
