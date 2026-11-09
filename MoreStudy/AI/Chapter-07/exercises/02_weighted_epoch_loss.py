"""Practice 02 — Mini-Batch Loss 가중 평균."""

def weighted_epoch_loss(batch_losses:list[float],batch_sizes:list[int])->float:
    # TODO: 리스트 길이, 양의 Batch 크기, 유한한 손실 검증
    # TODO: sum(loss_i * size_i) / sum(size_i)
    raise NotImplementedError

if __name__=='__main__':
    print(weighted_epoch_loss([.4,.9],[8,2]))
