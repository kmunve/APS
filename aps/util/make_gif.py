import imageio

def make_gif(in_files, out_file='out.gif', frame_duration=0.3):
    images = []
    for f in in_files:
        images.append(imageio.imread(f))
    imageio.mimsave(out_file, images, duration=frame_duration)

# Alternative - more stable?
# with imageio.get_writer('fl.gif', mode='I') as writer:
#     for f in png_files:
#         image = imageio.imread(f)
#         writer.append_data(image)


if __name__ == "__main__":
    png_files = []
    for i in range(24):
        png_files.append('fl_{0:02}.png'.format(i))

    make_gif(png_files, 'fl.gif')