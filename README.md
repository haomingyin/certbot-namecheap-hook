# Certbot Namecheap Hook

If [Namecheap](https://www.namecheap.com/) is your DNS registrar, the scripts can be used to automatically obtain/renew wildcard certificates using [Certbot](https://Certbot.eff.org/).

## Introduction

Every certificate applied from Certbot expires in three months. It's frustrating that you have to renew certs every three months. Though Certbot supports auto renewing them by setting up a [Cron](https://en.wikipedia.org/wiki/Cron) task. However, it doesn't support auto renewing wildcard certificates due to the limitation of[dns-01](https://tools.ietf.org/html/draft-ietf-acme-acme-03#section-7.4) challenge. This repository uses Namecheap API updating your DNS record to fight back the Certbot challenge.

## Get Started

### Pre-requirements

- Ensure you have your Namecheap account API key at hand. Refer to [get API key](https://www.namecheap.com/support/api/intro.aspx).

- Python 3 is required to get the script working

### Run Scripts

The `main.sh` is a sample script showing how to use Certbot to obtain/renew a wildcard cert. Please refer to it and create your own customized scripts.

When you trial-and-error your customized script, you are highly recommended to hit the staging environment instead of production environment. [Let's Encrypt](https://letsencrypt.org/) has strict [rate limit](https://letsencrypt.org/docs/rate-limits/), which can be easily run out (then you have to wait another week to get your production certs).

### Required Environment Variables

There are several environment variables required to get the `namecheap.py` working.

| Env Variable | Comment                                    | Example        |
| ------------ | ------------------------------------------ | -------------- |
| API_USER     | Normally, it's the same with your username | `username`     |
| API_KEY      | Namecheap account API key                  | `your-api-key` |
| USERNAME     | Namecheap account username                 | `username`     |
| CLIENT_IP    | The public IP which you use to hit the API | `10.42.193.39` |
| SLD          | Second level domain                        | `haomingyin`   |
| TLD          | Top level domain                           | `com`          |

To use the sample `main.sh` script, you have set up the following environment variables as well.

| Env Variable | Comment                                                   | Example                                        |
| ------------ | --------------------------------------------------------- | ---------------------------------------------- |
| APPLY_DOMAIN | The domain you are applying cert for. Wildcard is allowed | `*.haomingyin.com` or `Certbot.haomingyin.com` |
| EMAIL        | The email to register a let's encrypt account             | `email@gmail.com`                              |
| ACME_MODE    | Staging mode or production mode                           | `staging` or `prod`                            |

### How Do I Use It

I have my Jenkins server periodically run the script. The reason I'm not using Cron is that I have several severs and can't be bothered to set it up on each server. Also, by using Jenkins Pipeline, the latest scripts will always be sync and updated among all my servers. You welcome to check out my [Jenkins Pipeline file](https://github.com/haomingyin/jenkins-certbot).

## Reference

- Namecheap official [API](https://www.namecheap.com/support/api/intro.aspx).
- Certbot [user guide](https://Certbot.eff.org/docs/using.html)
