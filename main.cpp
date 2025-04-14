#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <map>

class RawImage {
    private:
        std::string type;
        int lines, columns;
        int max_value;
        std::vector<std::vector<unsigned char>> pixels;

    public:
        RawImage(std::ifstream &image_file) {

            std::string buffer;

            while(getline(image_file,buffer)) {
                if(buffer[0] == '#') { // ta bom eu sei que o # pode estar depois da posição 0.
                    continue;
                } else break;
            }

            type = buffer;

            while(getline(image_file,buffer)) {
                if(buffer[0] == '#') { // ta bom eu sei que o # pode estar depois da posição 0.
                    continue;
                } else break;
            }

            std::stringstream  line_column_values(buffer);

            line_column_values >> lines >> columns;

            while(getline(image_file,buffer)) {
                if(buffer[0] == '#') { // ta bom eu sei que o # pode estar depois da posição 0.
                    continue;
                } else break;
            }

            max_value = atoi(buffer.c_str());

            for(int i=0;i<lines;i++) {
                std::vector<unsigned char> line;
                std::vector<int> int_line;
                for(int j=0;j<columns;j++) {
                    int int_pixel;

                    image_file >> int_pixel;

                    line.push_back((unsigned char) int_pixel);
                }
                pixels.push_back(line);
            }
        }

        void create_compressed_image(std::string compressed_file_name) {

            int symbol_counter[256];

            std::map<unsigned char, float> symbol_probs, lower_symbol_probs;

            for(int i=0;i<256;i++) symbol_counter[i] = 0;

            for(int i=0;i<lines;i++) {
                for(int j=0;j<columns;j++) {
                    symbol_counter[pixels[i][j]]++;
                }
            }

            float old_prob = 0.0;

            for(int i=0;i<256;i++) {
                if(symbol_counter[i] != 0) {
                    lower_symbol_probs[(unsigned char) i] = old_prob;
                    old_prob += (float) symbol_counter[i]/(lines*columns);
                    symbol_probs[(unsigned char) i] = old_prob;
                }
            }

            std::ofstream compress_file;
            compress_file.open(compressed_file_name, std::ofstream::binary | std::ofstream::out);

            // Escrever o tipo de compressão, como eu criei se chama Leo.
            compress_file << (unsigned char) 'L';
            compress_file << (unsigned char) 'E';
            compress_file << (unsigned char) 'O';

            compress_file << (unsigned char) 0x00 << (unsigned char) 0x00 << (unsigned char) 0x00;

            compress_file << (unsigned char) type[0] << (unsigned char) type[1];

            void *bytes = (void *) &lines;
            unsigned char *lines_bytes = (unsigned char *) bytes;

            bytes = (void *) &columns;
            unsigned char *columns_bytes = (unsigned char *) bytes;

            compress_file << lines_bytes[0];
            compress_file << lines_bytes[1];
            compress_file << lines_bytes[2];
            compress_file << lines_bytes[3];

            compress_file << columns_bytes[0];
            compress_file << columns_bytes[1];
            compress_file << columns_bytes[2];
            compress_file << columns_bytes[3];

            for(int i=0;i<256;i++) {
                if(symbol_counter[i] != 0) compress_file << (unsigned char) i;
            }

            int padding = symbol_probs.size() % 4;

            for(int i=0;i<4 - padding;i++) compress_file << (unsigned char) 0x00;

            for(int i=0;i<256;i++) {
                if(symbol_counter[i] != 0) {
                    void *bytes =  (void *) &symbol_probs[(unsigned char) i];
                    unsigned char *vals = (unsigned char *) bytes;
                    compress_file << vals[0];
                    compress_file << vals[1];
                    compress_file << vals[2];
                    compress_file << vals[3];
                }
            }

            float high = 1.0, low = 0.0;

            for(int i=0;i<lines;i++) {
                for(int j=0;j<columns;j++) {
                    float size = high - low;

                    high = low + size*symbol_probs[pixels[i][j]];
                    low  = low + size*lower_symbol_probs[pixels[i][j]];
                }
            }

            float mean = (high + low)/2;

            bytes = (void *) &mean;
            unsigned char *mean_bytes = (unsigned char *) bytes;

            compress_file << mean_bytes[0];
            compress_file << mean_bytes[1];
            compress_file << mean_bytes[2];
            compress_file << mean_bytes[3];

            compress_file.close();
        }
};

int main(int argc, char **argv) {
    for(int i=1;i<argc;i++) {
        std::ifstream image_file(argv[i]);

        if(!image_file.is_open()) {
            return 1;
        }

        RawImage image(image_file);

        size_t dot_pos = std::string(argv[i]).find_first_of(".");

        image.create_compressed_image(std::string(argv[i]).substr(0,dot_pos)+".leo");

        image_file.close();
    }
}