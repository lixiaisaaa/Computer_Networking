class Solution:
    def reachingPoints(self, sx: int, sy: int, tx: int, ty: int) -> bool:
        if tx < sx or ty < sy:
            return False
        if sx == tx:
            # 横坐标相同，此时纵坐标 (ty - sy) 的差如果能被 sx 整除，可以通过多次 ty - sx 获得
            return (ty - sy) % sx == 0
        elif sy == ty:
            # 纵坐标相同，此时横坐标 (tx - sx) 的差如果能被 sy 整除，可以通过多次 tx - sy 获得
            return (tx - sx) % sy == 0
        return self.reachingPoints(sx, sy, tx%ty, ty) if tx > ty else self.reachingPoints(sx, sy, tx, ty%tx)

