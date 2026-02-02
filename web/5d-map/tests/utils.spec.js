import { describe, test, expect, vi } from 'vitest';
import { debounce } from '../modules/utils.js';

describe('Utility Functions', () => {
  describe('debounce', () => {
    test('should delay execution of function', () => {
      vi.useFakeTimers();
      const func = vi.fn();
      const debouncedFunc = debounce(func, 100);

      debouncedFunc();
      expect(func).not.toHaveBeenCalled();

      vi.advanceTimersByTime(50);
      expect(func).not.toHaveBeenCalled();

      vi.advanceTimersByTime(51);
      expect(func).toHaveBeenCalledTimes(1);
    });

    test('should reset timer on subsequent calls', () => {
      vi.useFakeTimers();
      const func = vi.fn();
      const debouncedFunc = debounce(func, 100);

      debouncedFunc();
      vi.advanceTimersByTime(50);
      debouncedFunc(); // reset timer

      vi.advanceTimersByTime(50);
      expect(func).not.toHaveBeenCalled();

      vi.advanceTimersByTime(51);
      expect(func).toHaveBeenCalledTimes(1);
    });

    test('should pass arguments to the original function', () => {
        vi.useFakeTimers();
        const func = vi.fn();
        const debouncedFunc = debounce(func, 100);

        debouncedFunc('test', 123);
        vi.advanceTimersByTime(100);
        expect(func).toHaveBeenCalledWith('test', 123);
    });
  });
});
