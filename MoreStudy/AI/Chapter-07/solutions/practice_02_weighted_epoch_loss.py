"""Practice 02 — 불완전한 마지막 Batch의 손실을 바르게 집계합니다."""
import math

def weighted_epoch_loss(batch_losses:list[float],batch_sizes:list[int])->float:
    if not batch_losses or len(batch_losses)!=len(batch_sizes):
        raise ValueError('Mismatched or empty batches')
    if any(b<=0 for b in batch_sizes) or not all(math.isfinite(float(v)) for v in batch_losses):
        raise ValueError('Invalid batch loss or size')
    return sum(float(v)*int(n) for v,n in zip(batch_losses,batch_sizes))/sum(batch_sizes)

if __name__=='__main__':
    print(weighted_epoch_loss([.4,.9],[8,2]))
