from PIL import Image
import matplotlib.pyplot as plt
import io


console_sales = {
  2020: (('Switch', 'XBox', 'Playstation'),(1.549, 0, 0)),
  2021: (('Switch', 'XBox', 'Playstation'),( 1.544, 0.325, 0.653)),
  2022: (('Switch', 'XBox', 'Playstation'),( 1.328, 0.605, 0.708)),
  2023: (('Switch', 'XBox', 'Playstation'),( 1.140, 0.456, 1.257)),
}

images = []

for year, data in console_sales.items():
    fig = plt.figure(figsize = (6,5))
    companies, sales = data
    plt.bar(companies, sales, color = ['red', 'green', 'blue'])

    plt.title(f'Console sales in {year}')
    plt.ylabel('Sales in millions')

    buffer = io.BytesIO()

    plt.savefig(buffer, format = 'png')
    image = Image.open(buffer)
    images.append(image)
images[0].save('animated_graph.gif', save_all = True, append_images = images[1:], duration = 500, loop = 0)
    
