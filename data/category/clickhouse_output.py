import requests
import argparse

CLICKHOUSE_HOST = "172.23.216.106"
CLICKHOUSE_PORT = 8123
DATABASE = "ty"
USERNAME = "default"  # 必须有用户名
PASSWORD = ""         # 空密码

OUTPUT_FILE = "clickhouse_export.csv"

def export_to_csv(platform: str):
    QUERY = f"""
    SELECT
        name,
        description,
        platform,
        gather_time,
        category_1,
        price,
        user_name
    FROM ty.mid_deepweb_goods
    WHERE platform = '{platform}'
    ORDER BY gather_time DESC
    LIMIT 50
    FORMAT CSVWithNames
    """

    url = f"http://{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}/"
    params = {"database": DATABASE}

    print(f"正在从 ClickHouse 导出数据 -> {OUTPUT_FILE}")
    response = requests.post(
        url,
        params=params,
        data=QUERY.encode("utf-8"),
        auth=(USERNAME, PASSWORD)
    )

    if response.status_code != 200:
        print("❌ 导出失败:", response.text)
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8-sig") as f:
        f.write(response.text)

    print(f"✅ 导出成功！文件已保存为：{OUTPUT_FILE}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从 ClickHouse 导出 CSV")
    parser.add_argument(
        "--platform",
        type=str,
        default="",  # 默认空字符串
        help="要导出的 platform 名称，默认空字符串"
    )
    args = parser.parse_args()
    export_to_csv(args.platform)
