import random
import time

NUM_LOGS = 10000


hidden_attacker_ips = [
    [random.randint(1, 223), random.randint(0, 255), random.randint(0, 255), random.randint(1, 254)],
    [random.randint(1, 223), random.randint(0, 255), random.randint(0, 255), random.randint(1, 254)]
]

logs = []
for _ in range(NUM_LOGS):

    if random.random() < 0.30:
        ip_bytes = random.choice(hidden_attacker_ips).copy()
    else:

        ip_bytes = [
            random.randint(1, 223),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(1, 254)
        ]

    status = random.choices(
        population=[200, 404, 500, 503],
        weights=[70, 15, 10, 5]
    )[0]

    logs.append({
        'ip_bytes': ip_bytes,
        'ip_str': f"{ip_bytes[0]}.{ip_bytes[1]}.{ip_bytes[2]}.{ip_bytes[3]}",
        'status': status
    })

print(f"Сгенерировано логов: {len(logs)}\n")



def counting_sort_by_status(logs_list):
    min_status = 100
    max_status = 599
    count = [0] * (max_status - min_status + 1)
    for log in logs_list:
        count[log['status'] - min_status] += 1

    status_groups = {}
    for i in range(len(count)):
        if count[i] > 0:
            status_groups[i + min_status] = []

    for log in logs_list:
        status_groups[log['status']].append(log)

    sorted_logs = []
    for status in sorted(status_groups.keys()):
        sorted_logs.extend(status_groups[status])
    return sorted_logs, status_groups


def counting_sort_by_byte(logs_list, byte_index):
    count = [0] * 256
    output = [None] * len(logs_list)
    for log in logs_list:
        count[log['ip_bytes'][byte_index]] += 1
    for i in range(1, 256):
        count[i] += count[i - 1]
    for i in range(len(logs_list) - 1, -1, -1):
        log = logs_list[i]
        byte_value = log['ip_bytes'][byte_index]
        count[byte_value] -= 1
        output[count[byte_value]] = log
    return output


def radix_sort_by_ip(logs_list):
    sorted_logs = logs_list.copy()
    for byte_index in [3, 2, 1, 0]:
        sorted_logs = counting_sort_by_byte(sorted_logs, byte_index)
    return sorted_logs



start_cs = time.perf_counter()
sorted_by_status, status_groups = counting_sort_by_status(logs.copy())
end_cs = time.perf_counter()
time_cs = end_cs - start_cs

start_rs = time.perf_counter()
sorted_by_ip = radix_sort_by_ip(logs.copy())
end_rs = time.perf_counter()
time_rs = end_rs - start_rs

print(f"Counting Sort по статусам: {time_cs:.4f} сек")
print(f"Radix Sort    по IP:       {time_rs:.4f} сек\n")


print("1. Распределение запросов по HTTP-статусам:")
print("-" * 40)
for status in sorted(status_groups.keys()):
    count = len(status_groups[status])
    percent = (count / len(logs)) * 100
    print(f"   HTTP {status}: {count:>6} ({percent:5.1f}%)")


ip_counts = {}
for log in sorted_by_ip:
    ip = log['ip_str']
    ip_counts[ip] = ip_counts.get(ip, 0) + 1


top_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)


ATTACK_THRESHOLD_PERCENT = 5.0
attackers = []

print("\n2. Топ-10 IP-адресов (по количеству запросов):")
print("-" * 40)
for rank, (ip, count) in enumerate(top_ips[:10], 1):
    percent = (count / len(logs)) * 100

    if percent >= ATTACK_THRESHOLD_PERCENT:
        attackers.append((ip, count, percent))
        marker = ' [АТАКА]'
    else:
        marker = ''
    print(f"   {rank}. {ip:<18}  {count:>5} запросов ({percent:.1f}%){marker}")

print(f"\n3. Автоматически выявлено атакующих IP: {len(attackers)}")
print("-" * 40)


for attacker_ip, total_attacks, percent in attackers:
    print(f"\nIP-атакующего: {attacker_ip} (Всего запросов: {total_attacks}, {percent:.1f}% от общего трафика)")

    attacker_statuses = {}
    for log in logs:
        if log['ip_str'] == attacker_ip:
            status = log['status']
            attacker_statuses[status] = attacker_statuses.get(status, 0) + 1

    for status in sorted(attacker_statuses.keys()):
        count = attacker_statuses[status]
        status_percent = (count / total_attacks) * 100
        print(f"      HTTP {status}: {count:>5} ({status_percent:5.1f}%)")
