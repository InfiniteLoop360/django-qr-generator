class Solution:
    def minCost(self, height):
        n = len(height)
        if n <= 1:
            return 0
        
        prev2 = 0  # dp[i-2]
        prev1 = 0  # dp[i-1]
        
        for i in range(1, n):
            one_step = prev1 + abs(height[i] - height[i - 1])
            
            two_step = float('inf')
            if i > 1:
                two_step = prev2 + abs(height[i] - height[i - 2])
            
            curr = min(one_step, two_step)
            
            prev2 = prev1
            prev1 = curr
        
        return prev1
