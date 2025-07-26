import pandas as pd
import numpy as np


def clean_mansion_data(excel_path: str, output_csv: str) -> None:
    """Extract and clean raw mansion data."""
    df = pd.read_excel(excel_path)

    df["価格"] = df["価格"].apply(lambda x: int(x[:-2].replace(",", "")) * 10000)
    df["建物階数"] = df["階数"].str.extract("(\d+)")
    df["住居階数"] = df["階数"].str.extract("/ (\d+)")
    df["住居階数"] = df["住居階数"].fillna(df["住居階数"].median())
    df["建物階数"] = df["建物階数"].astype(int)
    df["住居階数"] = df["住居階数"].astype(int)

    df["築年数"] = df["築年月"].str.extract("築(\d+)")
    df["築年数"] = df["築年数"].fillna("0").astype(int)

    df["占有面積"] = df["占有面積"].str.extract("(\d+\.\d+)").astype(float)

    df["路線"] = df["交通"].str.extract("\t*(.*線)")
    df["駅"] = df["交通"].str.extract("/(.*駅)")
    df["駅徒歩分"] = df["交通"].str.extract("駅\\s徒歩(\d+)分")
    df["駅徒歩分"] = df["駅徒歩分"].fillna("60").astype(int)

    df["所在地"] = df["所在地"].str.extract("東京都(.*区|.*市)")

    df["修繕積立金"] = df["修繕積立金"].str.extract("(\d+\,\d+)")
    df["修繕積立金"] = df["修繕積立金"].fillna(
        str(round(df[~df["修繕積立金"].isna()]["修繕積立金"].apply(lambda x: int(x.replace(",", ""))).mean()))
    )
    df["修繕積立金"] = df["修繕積立金"].apply(lambda x: int(x.replace(",", "")))

    df["管理費"] = df["管理費"].str.extract("(\d+\,\d+)")
    df["管理費"] = df["管理費"].fillna(
        str(round(df[~df["管理費"].isna()]["管理費"].apply(lambda x: int(x.replace(",", ""))).mean()))
    )
    df["管理費"] = df["管理費"].apply(lambda x: int(x.replace(",", "")))

    df["修繕＋管理費"] = df["修繕積立金"] + df["管理費"]

    df = df.replace(
        ["SRC・RC造", "（ＳＲＣ・ＲＣ造）", "ＳＲＣ・ＲＣ造", "ＳＲＣ造・ＲＣ造", "SRC、RC", "ＳＲＣ・ＲＣ"],
        "SRC・RC",
    ).replace(["鉄骨・RC造", "ＲＣ造・鉄骨造"], "ＲＣ・鉄骨造").replace(["－", "備考参照"], np.nan)

    df["総戸数"] = df["総戸数"].str.extract("(\d+)")
    df["総戸数"] = df["総戸数"].fillna(
        format(df[~df["総戸数"].isna()]["総戸数"].apply(lambda x: int(x)).median(), ".0f")
    )
    df["総戸数"] = df["総戸数"].astype(int)

    df["駐車場料金"] = df["駐車場"].str.extract("有(.*\d)円/月")
    df["駐車場"] = df["駐車場"].str.extract("(無|有|近有|空無)")
    df["駐車場料金有無"] = df["駐車場料金"].isna()

    for idx, row in df.iterrows():
        if not row["駐車場料金有無"]:
            df.loc[idx, "駐車場料金"] = int(row["駐車場料金"].replace(",", ""))

    df["バイク置き場"] = df["バイク置き場"].str.extract("(無|有|空無)")

    df["土地権利"] = df["土地権利"].str.extract(
        "(所有権|旧法地上権|旧法賃借権|普通賃借権|普通地上権|有|無|定期借地権（地上権）|定期借地権（賃借権）)"
    )

    df["管理形態"] = df["管理形態"].str.extract(
        "(全部委託・常駐管理|全部委託・日勤管理|全部委託・巡回管理|一部委託・日勤管理|一部委託・常駐管理|一部委託・巡回管理)"
    )

    df = df.drop(
        labels=["建物名", "平米単価", "階数", "築年月", "交通", "駐車場料金有無"],
        axis=1,
    )

    df = df.rename(
        columns={
            "価格": "price",
            "占有面積": "occupancy_area",
            "間取り": "room_layout",
            "所在地": "address",
            "管理費": "management_expenses",
            "修繕積立金": "reserve_fund_for_repairs",
            "建物構造": "building_structure",
            "総戸数": "total_number_of_houses",
            "バイク置き場": "bike_parking",
            "駐車場": "parking",
            "土地権利": "land_rights",
            "管理形態": "management",
            "建物階数": "rank",
            "住居階数": "floor_number",
            "ペット": "pet",
            "築年数": "building_age",
            "路線": "route",
            "駅": "station",
            "駅徒歩分": "walk_distance",
            "修繕＋管理費": "running_cost",
            "駐車場料金": "parking_cost",
        }
    )

    df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean used mansion dataset")
    parser.add_argument("--excel", default="work/used_mansion.xlsx", help="Path to excel file")
    parser.add_argument("--output", default="work/etl_used_mansion.csv", help="Output CSV path")
    args = parser.parse_args()

    clean_mansion_data(args.excel, args.output)
