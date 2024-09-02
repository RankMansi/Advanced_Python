import os
import re
from collections import defaultdict

def extract_review_data(line):
    pattern = re.compile(r'CustomerID: ([A-Z0-9]+), ProductID: ([A-Z0-9]+), ReviewDate: (\d{4}-\d{2}-\d{2}), ReviewRating: (\d), ReviewText: "(.+)"')
    match = pattern.match(line.strip())
    if match:
        customer_id, product_id, review_date, review_rating, review_text = match.groups()
        review_rating = int(review_rating)
        if 1 <= review_rating <= 5:
            return {
                'CustomerID': customer_id,
                'ProductID': product_id,
                'ReviewDate': review_date,
                'ReviewRating': review_rating,
                'ReviewText': review_text
            }, None
    return None, "Invalid format or rating"

def process_files(directory):
    total_reviews = valid_reviews = invalid_reviews = 0
    product_ratings = defaultdict(list)
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    total_reviews += 1
                    review_data, error = extract_review_data(line)
                    if review_data:
                        valid_reviews += 1
                        product_ratings[review_data['ProductID']].append(review_data['ReviewRating'])
                    else:
                        invalid_reviews += 1
    
    return product_ratings, total_reviews, valid_reviews, invalid_reviews

def calculate_average_ratings(product_ratings):
    return {product_id: sum(ratings) / len(ratings) for product_id, ratings in product_ratings.items()}

def get_top_products(average_ratings, top_n=3):
    return sorted(average_ratings.items(), key=lambda x: x[1], reverse=True)[:top_n]

def write_summary(file_path, total_reviews, valid_reviews, invalid_reviews, top_products):
    with open(file_path, 'w') as file:
        file.write(f"Total reviews processed: {total_reviews}\n")
        file.write(f"Total valid reviews: {valid_reviews}\n")
        file.write(f"Total invalid reviews: {invalid_reviews}\n")
        file.write("Top 3 Products with Highest Average Ratings:\n")
        for product_id, avg_rating in top_products:
            file.write(f"Product ID: {product_id}, Average Rating: {avg_rating:.2f}\n")

def main():
    directory = r'D:\Projects\RankMansi\Semesters\Sem-5\Lab-Advanced Python\directory_for_reviews'  # Path to your directory containing review files
    summary_file_path = r'D:\Projects\RankMansi\Semesters\Sem-5\Lab-Advanced Python\directory_for_reviews\summary.txt'
    
    product_ratings, total_reviews, valid_reviews, invalid_reviews = process_files(directory)
    
    average_ratings = calculate_average_ratings(product_ratings)
    
    top_products = get_top_products(average_ratings)
    
    write_summary(summary_file_path, total_reviews, valid_reviews, invalid_reviews, top_products)

if __name__ == "__main__":
    main()