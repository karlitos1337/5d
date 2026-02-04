import { describe, it, expect, vi } from 'vitest';
import { debounce } from '../modules/utils.js';

describe('utils', () => {
  describe('debounce', () => {
    it('should execute the function only once after the delay', () => {
      vi.useFakeTimers();
      const func = vi.fn();
      const debouncedFunc = debounce(func, 100);

      debouncedFunc();
      debouncedFunc();
      debouncedFunc();

      expect(func).not.toHaveBeenCalled();

      vi.advanceTimersByTime(50);
      expect(func).not.toHaveBeenCalled();

      vi.advanceTimersByTime(51);
      expect(func).toHaveBeenCalledTimes(1);

      vi.useRealTimers();
    });

    it('should pass arguments to the original function', () => {
        vi.useFakeTimers();
        const func = vi.fn();
        const debouncedFunc = debounce(func, 100);

        debouncedFunc('test');
        vi.advanceTimersByTime(100);
        expect(func).toHaveBeenCalledWith('test');
        vi.useRealTimers();
    });
  });
});
