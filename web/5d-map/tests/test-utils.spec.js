import { describe, test, expect, vi } from 'vitest';
import { debounce } from '../modules/utils.js';

describe('Utility Functions', () => {
  describe('debounce', () => {
    test('executes function after wait time', () => {
      vi.useFakeTimers();
      const func = vi.fn();
      const debouncedFunc = debounce(func, 100);

      debouncedFunc();
      expect(func).not.toHaveBeenCalled();

      vi.advanceTimersByTime(50);
      expect(func).not.toHaveBeenCalled();

      vi.advanceTimersByTime(50);
      expect(func).toHaveBeenCalledTimes(1);
    });

    test('prevents multiple executions within wait time', () => {
      vi.useFakeTimers();
      const func = vi.fn();
      const debouncedFunc = debounce(func, 100);

      debouncedFunc();
      vi.advanceTimersByTime(50);
      debouncedFunc(); // Reset timer
      vi.advanceTimersByTime(50);
      expect(func).not.toHaveBeenCalled(); // Should not run yet, total 100ms passed but reset at 50ms

      vi.advanceTimersByTime(50); // Now 100ms since last call
      expect(func).toHaveBeenCalledTimes(1);
    });

    test('passes arguments correctly', () => {
      vi.useFakeTimers();
      const func = vi.fn();
      const debouncedFunc = debounce(func, 100);

      debouncedFunc('hello', 'world');
      vi.advanceTimersByTime(100);
      expect(func).toHaveBeenCalledWith('hello', 'world');
    });
  });
});
