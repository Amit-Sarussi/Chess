
START_SHIFT = 0
END_SHIFT = 6
PROMOTION_SHIFT = 12


def encode_move(start, end, promotion=0):
    return (start << START_SHIFT) | (end << END_SHIFT) | (promotion << PROMOTION_SHIFT)

def decode_move(move):
    start = (move >> START_SHIFT) & 0x3F  # 6 bits mask
    end = (move >> END_SHIFT) & 0x3F
    promotion = (move >> PROMOTION_SHIFT) & 0xF  # 4 bits mask
    return start, end, promotion
