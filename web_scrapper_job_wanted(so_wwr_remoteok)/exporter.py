import csv

def save_to_file(name, datas):
  file = open(f"{name}.csv", mode = "w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Link"])
  for data in datas:
    writer.writerow(list(data.values()))
  return