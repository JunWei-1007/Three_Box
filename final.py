import download as dow
import up_data as up
import data as da

def main():
    dow.dow()
    oldest_date, latest_date, number_counts_dict, result = da.data()
    up.up(oldest_date, latest_date, number_counts_dict, result)

if __name__ == "__main__":
    main()