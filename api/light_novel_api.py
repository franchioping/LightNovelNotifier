import requests


class LightNovelApi:
    def __init__(self):
        self.cookies = {
            "__cf_bm": "9YQsVHZvNF_sKm3v3dtSn__hIwdUflFjkJuTZJTF.ow-1673202843-0-AXBVygbiaFm68A+ICTR5BGQcOaROqDEjg6FmFmk2lx6KH9o4JROEHc3RK+q4dz1lryvCwje73udLLjWXKZ/iUva4iiOBDd8D6BOppKt/6DpFed29ghShzhU5Mes0wQSdJxKq28ng8Km9mEpnhsRjb+s=",
            "_lnvstuid": "v2_eadbebec43b8c10aa2f39f1fe3358206_0.7",
            "addtl_consent": "1~39.4.3.9.6.9.13.6.4.15.9.5.2.11.1.7.1.3.2.10.3.5.4.21.4.6.9.7.10.2.9.2.18.7.20.5.20.6.5.1.3.1.11.29.4.14.4.5.3.10.6.2.9.6.6.9.4.4.29.4.5.3.1.6.2.2.17.1.17.10.9.1.8.6.2.8.3.4.146.8.42.15.1.14.3.1.18.25.3.7.25.5.18.9.7.41.2.4.18.21.3.4.2.7.6.5.2.14.18.7.3.2.2.8.20.8.8.6.3.10.4.20.2.13.4.6.4.11.1.3.22.16.2.6.8.2.4.11.6.5.33.11.8.1.10.28.12.1.3.21.2.7.6.1.9.30.17.4.9.15.8.7.3.6.6.7.2.4.1.7.12.13.22.13.2.12.2.10.1.4.15.2.4.9.4.5.4.7.13.5.15.4.13.4.14.10.15.2.5.6.2.2.1.2.14.7.4.8.2.9.10.18.12.13.2.18.1.1.3.1.1.9.25.4.1.19.8.4.5.3.5.4.8.4.2.2.2.14.2.13.4.2.6.9.6.3.2.2.3.5.2.3.6.10.11.6.3.16.3.11.3.1.2.3.9.19.11.15.3.10.7.6.4.3.4.6.3.3.3.3.1.1.1.6.11.3.1.1.11.6.1.10.5.2.6.3.2.2.4.3.2.2.7.15.7.14.1.3.3.4.5.4.3.2.2.5.4.1.1.2.9.1.6.9.1.5.2.1.7.10.11.1.3.1.1.2.1.3.2.6.1.12.5.3.1.3.1.1.2.2.7.7.1.4.1.2.6.1.2.1.1.3.1.1.4.1.1.2.1.8.1.7.4.3.2.1.3.5.3.9.6.1.15.10.28.1.2.2.12.3.4.1.6.3.4.7.1.3.1.1.3.1.5.3.1.3.4.1.1.4.2.1.2.1.2.2.2.4.2.1.2.2.2.4.1.1.1.2.2.1.1.1.1.2.1.1.1.2.2.1.1.2.1.2.1.7.1.2.1.1.1.2.1.1.1.1.2.1.1.3.2.1.1.8.1.1.6.2.1.6.2.3.2.1.1.1.2.2.3.1.1.4.1.1.2.2.1.1.4.3.1.2.2.1.2.1.2.3.1.1.2.4.1.1.1.5.1.3.6.3.1.5.2.3.4.1.2.3.1.4.2.1.2.2.2.1.1.1.1.1.1.11.1.3.1.1.2.2.5.2.3.3.5.1.1.1.4.2.1.1.2.5.1.9.4.1.1.3.1.7.1.4.5.1.7.2.1.1.1.2.1.1.1.4.2.1.12.1.1.3.1.2.2.3.1.2.1.1.1.2.1.1.2.1.1.1.1.2.4.1.5.1.2.4.3.8.2.2.9.7.2.2.1.2.1.4.6.1.1.6.1.1.2.6.3.1.2.201.300.100",
            "euconsent-v2": "CPlREsAPlREsAAKAtAENCyCsAP_AAH_AACgAJNNd_H__bW9r-f5_aft0eY1P9_rz7uQzDhfNk-4F3L_W_LwX52E7NF36tq4KmR4ku1LBIUNlHNHUDUmwaokVryHsak2cpTNKJ7BEknMZOydYGF9vmxtj-QKY5v5_d3bx2D-t_9v-39z3z81Xn3d5_-_02PCdV5_9Dfn9fR_b89KP9_78v4v8_____3_e__3_7997_H8EmwCTDVuIAuzLHBm0DCKBECMKwkIoFABBQDC0QEADg4KdlYBPrCBAAgFAEYEQIcAUYEAgAAEgCQiACQIsEAAAIgEAAIAEAiEADAwCCwAsDAIAAQDQMUQoABAkAMiAiKUwICoEggJbKhBKC6Q0wgCrLACgERsFAAiCQEVgACAsHAMESAlYsECTFG-QAjBCgFEqFaik9NAA.flgAAAAAAAAA",
            "lncoreantifrg": "CfDJ8FBkhIgVIu9DkfAIt6P2U0i1XSeOUEZ8GnC0aCjMDLQ1Zk5aiVKMucQk8NxnHZsFTbzE8ppLZZhl__2p9j0wTqihG1RnMuypb2_t_DabAFaP_hEm7bxfJ0_3zsRGkdH997TZrqAjdkoh_uGBAUWyG2w",
            "lnusrconf": "16,default,false,black,purple,en,0,1"
        }

        self.headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-Requested-With': 'XMLHttpRequest'}

        self.session = requests.Session()

    def get_session(self) -> requests.Session:
        return self.session

    def get(self, url):
        return self.session.get(url=url, cookies=self.cookies, headers=self.headers)
