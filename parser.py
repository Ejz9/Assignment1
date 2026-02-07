import os
import re
import csv

from bs4 import BeautifulSoup

MyAnimeList_URL = 'https://myanimelist.net/topanime.php'
AnimePlanet_URL = 'https://www.anime-planet.com/anime/all'

def parse(source_dir, dest_dir, mode='tr'):
    print(f'Parsing {source_dir} to {dest_dir}...')

    os.makedirs(dest_dir, exist_ok=True)

    rows = []
    files = sorted(os.listdir(source_dir))
    id_counter = 1
    for file in files:
        try:
            with open(f"{source_dir}/{file}", "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                if mode == 'tr':
                    for tr in soup.find_all("tr", {"class": "ranking-list"}):
                        try:
                            row_data = {'id': f"mal_{id_counter}"}

                            id_counter += 1

                            title_tag = tr.find('h3', class_='anime_ranking_h3')
                            row_data['title'] = title_tag.get_text(strip=True) if title_tag else ""

                            score_tag = tr.find('span', class_=re.compile('score-label'))
                            row_data['score'] = score_tag.get_text(strip=True) if score_tag else ""

                            info_div = tr.find('div', class_='information')
                            if info_div:
                                info_lines = [line.strip() for line in info_div.strings if line.strip()]

                                if len(info_lines) > 0:
                                    type_eps_str = info_lines[0]
                                    if '(' in type_eps_str:
                                        parts = type_eps_str.split('(')
                                        row_data['type'] = parts[0].strip()
                                        row_data['eps'] = parts[1].replace(' eps)', '').replace(')', '').strip()
                                    else:
                                        row_data['type'] = type_eps_str
                                        row_data['eps'] = ""

                                if len(info_lines) > 1:
                                    row_data['year'] = info_lines[1].strip()

                            rows.append(row_data)

                        except Exception as e:
                            print(f"Error parsing row: {e}")
                elif mode == 'card':
                    for card in soup.find_all("li", class_="card"):
                        try:
                            row_data = {'id': f"ap_{id_counter}"}

                            id_counter += 1

                            link_tag = card.find('a')
                            if not link_tag or not link_tag.has_attr('title'):
                                continue
                            tooltip_raw = link_tag.get('title')
                            tooltip = BeautifulSoup(tooltip_raw, "html.parser")

                            row_data['title'] = tooltip.find('h5').get_text(strip=True) if tooltip.find('h5') else ""

                            type_tag = tooltip.find('li', class_='type')
                            if type_tag:
                                type_text = type_tag.get_text(strip=True)
                                if "(" in type_text:
                                    parts = type_text.split('(')
                                    row_data['type'] = parts[0].strip()
                                    row_data['eps'] = parts[1].replace(' eps)', '').replace(' ep)', '').replace(')', '').strip()
                                else:
                                    row_data['type'] = type_text
                                    row_data['eps'] = ""
                            else:
                                row_data['type'] = ""
                                row_data['eps'] = ""

                            year_tag = tooltip.find('li', class_='iconYear')
                            row_data['year'] = year_tag.get_text(strip=True) if year_tag else ""

                            row_data['score'] = tooltip.find('div', class_='ttRating').get_text(strip=True) if tooltip.find('div', class_='ttRating') else ""

                            rows.append(row_data)

                        except Exception as e:
                            print(f"Error parsing row: {e}")

        except Exception as e:
            print(f"Error: {e}")

    if rows:
        with open(f"{dest_dir}/data.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'title', 'score', 'type', 'eps', 'year'])
            writer.writeheader()
            writer.writerows(rows)
        print(f"Success! Saved {len(rows)} rows to {dest_dir}/data.csv")
    else:
        print(f"No rows parsed for {dest_dir}.")

if __name__ == "__main__":
    parse('data/mal', 'output/mal', mode='tr')
    parse('data/ap', 'output/ap', mode='card')
