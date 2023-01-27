import os
from scrapers.ScraperMercator import ScraperMercator

def main():
    print("""
    ╱╭━╮╱╱╱╱╱╱╱╭┳━━━━╮╱╱╱╱╭╮╱╱╱╱╭╮╭╮╭╮╱╱╭╮╱╭━━━╮
    ╱┃╭╯╱╱╱╱╱╱╱┃┃╭╮╭╮┃╱╱╱╱┃┃╱╱╱╱┃┃┃┃┃┃╱╱┃┃╱┃╭━╮┃
    ╭╯╰┳━━┳━━┳━╯┣╯┃┃┣╋━╮╭━╯┣━━┳━┫┃┃┃┃┣━━┫╰━┫╰━━┳━━┳━┳━━┳━━┳━━┳━╮
    ╰╮╭┫╭╮┃╭╮┃╭╮┃╱┃┃┣┫╭╮┫╭╮┃┃━┫╭┫╰╯╰╯┃┃━┫╭╮┣━━╮┃╭━┫╭┫╭╮┃╭╮┃┃━┫╭╯
    ╱┃┃┃╰╯┃╰╯┃╰╯┃╱┃┃┃┃┃┃┃╰╯┃┃━┫┃╰╮╭╮╭┫┃━┫╰╯┃╰━╯┃╰━┫┃┃╭╮┃╰╯┃┃━┫┃
    ╱╰╯╰━━┻━━┻━━╯╱╰╯╰┻╯╰┻━━┻━━┻╯╱╰╯╰╯╰━━┻━━┻━━━┻━━┻╯╰╯╰┫╭━┻━━┻╯
    ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃
    ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰╯
    By David Cadez
    
    All output is redirected to output.log
    """)

    scd = ScraperMercator(os.getenv("HOST", default="spring"),
                          os.getenv("PORT", default="8082"),
                          os.getenv("PATH", default="/product/add"),
                          100,
                          0,
                          3)
    scd.work()


if __name__ == "__main__":
    main()
