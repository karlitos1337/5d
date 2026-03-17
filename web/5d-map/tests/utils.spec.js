import { describe, it, expect, vi, afterEach } from 'vitest';
import { debounce } from '../modules/utils.js';

describe('utils', () => {
  describe('debounce', () => {
    afterEach(() => {
      vi.useRealTimers();
    });

    it('should delay execution', () => {
      vi.useFakeTimers();
      const fn = vi.fn();
      const debouncedFn = debounce(fn, 100);

      debouncedFn();
      expect(fn).not.toHaveBeenCalled();

      vi.advanceTimersByTime(50);
      expect(fn).not.toHaveBeenCalled();

      vi.advanceTimersByTime(51);
      expect(fn).toHaveBeenCalledTimes(1);
    });

    it('should reset timer on subsequent calls', () => {
      vi.useFakeTimers();
      const fn = vi.fn();
      const debouncedFn = debounce(fn, 100);

      debouncedFn();
      vi.advanceTimersByTime(50);
      debouncedFn(); // Reset timer

      vi.advanceTimersByTime(50); // Total 100 from first call, but only 50 from second
      expect(fn).not.toHaveBeenCalled();

      vi.advanceTimersByTime(51);
      expect(fn).toHaveBeenCalledTimes(1);
    });
  });
});
