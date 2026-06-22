
-- FOOD WASTAGE PROJECT
-- 15 SQL QUERIES

SELECT COUNT(*) FROM FoodProviders;
SELECT COUNT(*) FROM FoodReceivers;
SELECT COUNT(*) FROM FoodListings;

SELECT City, COUNT(*) FROM FoodProviders GROUP BY City;
SELECT City, COUNT(*) FROM FoodReceivers GROUP BY City;

SELECT * FROM FoodListings WHERE ExpiryDate >= DATE('now');
SELECT * FROM FoodListings WHERE ExpiryDate < DATE('now');

SELECT FoodType, COUNT(*) FROM FoodListings GROUP BY FoodType ORDER BY COUNT(*) DESC;

SELECT ProviderID, COUNT(*) FROM FoodListings GROUP BY ProviderID ORDER BY COUNT(*) DESC LIMIT 1;

SELECT Status, COUNT(*) FROM Claims GROUP BY Status;

SELECT * FROM Claims WHERE Status='Completed';
SELECT * FROM Claims WHERE Status='Pending';
SELECT * FROM Claims WHERE Status='Cancelled';

SELECT FoodID, COUNT(*) FROM Claims GROUP BY FoodID ORDER BY COUNT(*) DESC LIMIT 5;

SELECT ProviderID, COUNT(*) FROM Claims WHERE Status='Completed'
GROUP BY ProviderID ORDER BY COUNT(*) DESC;
