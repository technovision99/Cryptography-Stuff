use hex;
use reqwest;
#[derive(Debug)]
pub struct Ciphertext {
    index: usize,
    plaintext: Vec<u8>,
    ciphertext_blocks: Vec<[u8;16]>,
    zeroifier: Vec<u8>
}

const URL: &str = "http://crypto-class.appspot.com/po?er=";
const TO_DECRYPT: &str = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4";

impl Ciphertext {
    fn build_ct(ct: &str) -> Self {
        let blocks  = hex::decode(ct).unwrap();
        let block_list = blocks.chunks(16).map(|x| TryInto::<[u8;16]>::try_into(x).unwrap()).collect::<Vec<[u8;16]>>();
        return Ciphertext {
            index: 1,
            plaintext: vec![],
            ciphertext_blocks: block_list,
            zeroifier: vec![]
        }

    }

    fn decrypt_one_block(&mut self, block_num: usize) {

        let block = self.ciphertext_blocks[block_num]; //cache to replace later after we mangle the block
        println!("{:?}",block);
        while self.index < 17 {
            println!("Starting new with index {}", self.index);
            for guess in 0..=255 {

                self.ciphertext_blocks[block_num][16-self.index] = guess;
                println!("{:?}", self.ciphertext_blocks[block_num]);
                println!("{:?}",hex::encode(&self.ciphertext_blocks[block_num]));
                let req_array = &self.ciphertext_blocks.clone().into_iter().flatten().collect::<Vec<u8>>();
                println!("{:?}", &hex::encode(req_array));
                let request = URL.to_owned() + &hex::encode(&req_array);
                println!("{}",request);
                if let Some(_res) = Self::make_request(&request) {
                    //account for edge case with penultimate byte
                    if self.index ==1 {
                        self.ciphertext_blocks[block_num][14] ^= 1;
                        let req_array = &self.ciphertext_blocks.clone().into_iter().flatten().collect::<Vec<u8>>();
                        println!("{:?}", &hex::encode(req_array));
                        let request = URL.to_owned() + &hex::encode(&req_array);
                        if let Some(request) = Self::make_request(&request) {
                            self.ciphertext_blocks[block_num][14] ^= 1; //reset and resume
                        }
                        else {
                            println!("fp found");
                            //self.ciphertext_blocks[block_num][14] ^= 1;
                            continue; //false positive
                        }
                    }
                    let payload = guess ^ self.index as u8;
                    self.plaintext.push(payload); ]

                    println!("{}",guess);
                    if self.index ==16 {
                        self.ciphertext_blocks[block_num] = block; //no need to do anything more
                        self.plaintext.reverse();
                        self.plaintext = self.plaintext.iter().zip(block.iter()).map(|(&x,&y)| x^y).collect();
                        self.index +=1;
                        break;
                    }

                    for val in 1..=self.index {
                        self.ciphertext_blocks[block_num][16-val] = self.plaintext[val-1]^ ((self.index+1) as u8);
                    }
                    let u = self.ciphertext_blocks[block_num][16-self.index];
                    println!("{}", u ^ payload);
                    self.index +=1;
                    println!("found");
                    break;
                }
            }
        }

    }
    fn make_request(request: &str) -> Option<&str> {
        let client = reqwest::blocking::Client::new();
        let req_result = client.get(request).send().ok()?;
        let passed = match req_result.status() {
            reqwest::StatusCode::FORBIDDEN => None,
            reqwest::StatusCode::NOT_FOUND => Some(request),
            _ => None
        };
        passed
    }
}
//bU+s"d^8AWZ
fn main() {
    let mut test: Ciphertext = Ciphertext::build_ct(TO_DECRYPT);
    println!("{:?}",test.ciphertext_blocks);
    test.decrypt_one_block(2);
    println!("{:?}", test.plaintext);
    let pt = std::str::from_utf8(&test.plaintext).expect("wrong");
    println!("{}",pt)


}