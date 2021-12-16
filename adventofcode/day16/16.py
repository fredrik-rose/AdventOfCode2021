# Day 16: Packet Decoder
import abc
import functools as ft
import itertools as it
import operator as op
import os
import sys

# pylint: disable=c-extension-no-member
sys.path.append(os.path.join(sys.path[0], '..', 'algorithms'))
import algorithms as algo  # # noqa: E402, pylint: disable=wrong-import-position


class Packet(abc.ABC):
    def __init__(self, length, version, type_id):
        self.length = length
        self.version = version
        self.type_id = type_id


class Literal(Packet):
    def __init__(self, length, version, type_id, value):
        super().__init__(length, version, type_id)
        self.value = value

    def __repr__(self):
        return f"Literal({self.length}, {self.version}, {self.type_id}, {self.value})"


class Operator(Packet):
    def __init__(self, length, version, type_id, operands):
        super().__init__(length, version, type_id)
        self.operands = operands

    def __repr__(self):
        return f"Operator({self.length}, {self.version}, {self.type_id}, {self.operands})"


def parse(file_path):
    with open(file_path) as file:
        return file.readline().rstrip()


def part_one(text):
    packet = parse_packet(tokenizer(text))
    answer = sum_version_numbers(packet)
    print(f"Part one: {answer}")


def part_two(text):
    packet = parse_packet(tokenizer(text))
    answer = eval_packet(packet)
    print(f"Part two: {answer}")


def tokenizer(text):
    binary = algo.hex_to_bin(text)
    for bit in binary:
        yield bit


def extract_binary(lexer, n):
    return ''.join(it.islice(lexer, n))


def extract_int(lexer, n):
    return algo.bin_to_int(extract_binary(lexer, n))


def parse_packet(packet):
    version = extract_int(packet, 3)
    type_id = extract_int(packet, 3)
    packet_length = 6
    if type_id == 4:
        literal, length = parse_literal(packet)
        packet_length += length
        return Literal(packet_length, version, type_id, literal)
    else:
        operator, length = parse_operator(packet)
        packet_length += length
        return Operator(packet_length, version, type_id, operator)


def parse_literal(text):
    value = ''
    length = 0
    while True:
        last = next(text) == '0'
        value += extract_binary(text, 4)
        length += 5
        if last:
            break
    return algo.bin_to_int(value), length


def parse_operator(text):
    mode = next(text)
    length = 1
    packets = []
    if mode == '0':
        subpackets_length = extract_int(text, 15)
        length += 15 + subpackets_length
        while subpackets_length > 0:
            packet = parse_packet(text)
            packets.append(packet)
            subpackets_length -= packet.length
    else:
        assert mode == '1'
        number_of_packets = extract_int(text, 11)
        length += 11
        for _ in range(number_of_packets):
            packet = parse_packet(text)
            packets.append(packet)
            length += packet.length
    return packets, length


def sum_version_numbers(packet):
    if isinstance(packet, Literal):
        return packet.version
    else:
        return packet.version + sum(sum_version_numbers(operand) for operand in packet.operands)


def eval_packet(packet):
    if isinstance(packet, Literal):
        return packet.value
    else:
        assert isinstance(packet, Operator)
        type_to_operation = {0: op.add,
                             1: op.mul,
                             2: min,
                             3: max,
                             5: op.gt,
                             6: op.lt,
                             7: op.eq,
                             }
        operands = [eval_packet(operand) for operand in packet.operands]
        return ft.reduce(type_to_operation[packet.type_id], operands)


def main():
    text = parse('16.txt')
    part_one(text)
    part_two(text)


if __name__ == "__main__":
    main()
