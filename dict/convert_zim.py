import zim2txt
def convert_zim_to_txt(zim_file_path, output_txt_path):
    try:
        # Convert and save the output to a text file
        zim2txt.ZimTools.Export(zim_file, "tmp", ".")

    except Exception as e:
        print(f"Error occurred while converting: {e}")

# Example usage
if __name__ == "__main__":
    zim_file = "wiktionary_es_all_maxi_2024-06.zim"  # Replace with your Zim file path
    output_txt = 'wiktionary_es_all_maxi_2024-06.txt'            # Desired output text file path
    convert_zim_to_txt(zim_file, output_txt)
