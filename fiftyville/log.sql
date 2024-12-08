-- Find crime details
SELECT * FROM crime_scene_reports WHERE day = 28 AND month = 7 AND street = "Humphrey Street";

-- Search through bakery log at 10.15am
SELECT * FROM bakery_security_logs WHERE day = 28 AND month = 7;
--5P2BI95   94KL13X    6P58WS2      4328GD8

--People who came to bakery
SELECT * FROM people WHERE license_plate = (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7);
--|   id   | name  |  phone_number  | passport_number | license_plate |
--| 809194 | Alice | (031) 555-9915 | 1679711307      | 1M92998       |

--FLights of the person
SELECT * FROM passengers WHERE passport_number = 1679711307 ;

--| 16        | 1679711307      | 3A   |
--| 52        | 1679711307      | 5B   |

--Interviews on that day
SELECT transcript FROM interviews WHERE month = 7 AND day = 28;
--theif left within 10 mins
--withdrew money from ATM on Leggett Street early morning
--Call of less than 1 min
-- Earliest flight next day
--Talked to the accomplice

--License plates of cars that left bakery within 10 mins of crime
SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7;
--5P2BI95  94KL13X 6P58WS2  4328GD8  G412CB7    L93JTIZ     322W7JE    0NTHK55 1106N58

-- Early withdrawals form atm
SELECT * FROM atm_transactions WHERE atm_location = "Leggett Street" AND day = 28 AND month = 7 AND transaction_type = "withdraw";

-- People names
SELECT p.name FROM people p JOIN bank_accounts b ON  p.id = b.person_id WHERE b.account_number = (SELECT account_number FROM atm_transactions WHERE atm_location = "Leggett Street" AND day = 28 AND month = 7 AND transaction_type = "withdraw");

--phone calls of short duration
SELECT * FROM phone_calls WHERE month = 7 AND day = 28  AND duration < 60;

-- Earliest flight next day
SELECT f.id, f.hour, f.minute, a.city AS destination
   ...> FROM flights f
   ...> JOIN airports a ON f.destination_airport_id = a.id
   ...> WHERE f.year = 2023 AND f.month = 7 AND f.day = 29
   ...>   AND f.origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
   ...> ORDER BY f.hour, f.minute
   ...> LIMIT 1;
   --flight_id = 36

-- Flight details
SELECT passport_number FROM passengers p WHERE flight_id = 36;

--Phone number of thief
SELECT phone_number FROM people WHERE passport_number = (SELECT passport_number FROM passengers p WHERE flight_id = 36);

-- Considering gathered info till now
--Suspects are
--| Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
--| Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |

--Both Taylor and Bruce had short duration calls around theft time

SELECT * FROM passengers where flight_id = 36;
--Both boarded the earliest flight next day to NEW YORK CITY

SELECT *  FROM atm_transactions WHERE atm_location = "Leggett Street" AND day = 28 AND month = 7 AND transaction_type = "withdraw";
-- account_numbers 28500762| 28296815| 76054385 | 49610011| 16153065  | 25506511 | 81061156  | 26013199


SELECT * FROM phone_calls WHERE caller = "(286) 555-6063" AND day = 28 AND month = 7;
--(676) 555-6554
SELECT * FROM phone_calls WHERE caller = "(367) 555-5533" AND day = 28 AND month = 7;
--(375) 555-8161

SELECT name FROM people WHERE phone_number = "(676) 555-6554";
--James
SELECT name FROM people WHERE phone_number = "(375) 555-8161";
--Robin

SELECT name
FROM people
WHERE phone_number = (
  SELECT receiver
  FROM phone_calls
  WHERE year = 2023 AND month = 7 AND day = 28
    AND duration < 60
    AND caller = (SELECT phone_number FROM people WHERE name = 'Taylor')
);
