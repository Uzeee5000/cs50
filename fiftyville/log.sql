-- Keep a log of any SQL queries you execute as you solve the mystery.
--To find out the crime report that corresponds to the incident
SELECT* FROM crime_scene_reports
WHERE day=28 AND month=07 AND year=2023 AND id =295 AND street LIKE '%Humphrey Street%';
--To examin the interviews from witnesses
SELECT* FROM interviews
WHERE day=28 AND month=07 AND year=2023;
--to examine the withdraws at Leggett Street
SELECT* FROM atm_transactions
WHERE day=28 AND month=07 AND year=2023 AND atm_location LIKE '%Leggett Street%' AND transaction_type LIKE '%Withdraw%';
--to examine the camera logs in bakery
SELECT* FROM bakery_security_logs
WHERE day=28 AND month=07 AND year=2023 AND hour=10 AND minute BETWEEN 15 AND 25;
--to examine the calls during that interval
SELECT* FROM phone_calls
WHERE day=28 AND month=07 AND year=2023 AND duration<=60;
--to examine the flights
SELECT* FROM flights
WHERE day=29 AND month=07 AND year=2023 ORDER BY hour ASC;
--to extract the passports of flights leaving early next day
SELECT* FROM passengers
JOIN flights ON passengers.flight_id=flights.id
WHERE day=29 AND month=07 AND year=2023 AND hour<10;
--to match the passport number against individuals with flights leaving early
SELECT* FROM people
WHERE passport_number IN (
SELECT passport_number FROM passengers
JOIN flights ON passengers.flight_id=flights.id
WHERE day=29 AND month=07 AND year=2023 AND hour<10
);
--- Fetching the bank accounts of suspected individual
SELECT* FROM bank_accounts
JOIN people ON bank_accounts.person_id=people.id
WHERE passport_number IN (
SELECT passport_number FROM passengers
JOIN flights ON passengers.flight_id=flights.id
WHERE day=29 AND month=07 AND year=2023 AND hour<10
);
--Joining all dots together
SELECT* FROM bank_accounts
JOIN people ON bank_accounts.person_id=people.id
WHERE passport_number IN (
SELECT passport_number FROM passengers
JOIN flights ON passengers.flight_id=flights.id
WHERE day=29 AND month=07 AND year=2023 AND hour<12
) AND account_number IN (
SELECT account_number FROM atm_transactions
WHERE day=28 AND month=07 AND year=2023 AND atm_location LIKE '%Leggett Street%' AND transaction_type LIKE '%Withdraw%'
) AND license_plate IN (
SELECT license_plate FROM bakery_security_logs
WHERE day=28 AND month=07 AND year=2023 AND hour=10 AND minute BETWEEN 15 AND 25
) AND phone_number IN(
SELECT caller FROM phone_calls
WHERE day=28 AND month=07 AND year=2023 AND duration<=60
);
--To Find the Accomplice
SELECT* FROM people
WHERE phone_number IN (
    SELECT receiver  FROM phone_calls
    WHERE day=28 AND month=07 AND year=2023 AND duration<=60 AND caller = '(367) 555-5533'
) ;
--To Chek the escape city
SELECT abbreviation, full_name, city
  FROM airports
 WHERE city = 'Fiftyville';
SELECT flights.id, full_name, city, flights.hour, flights.minute
  FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
 WHERE flights.origin_airport_id =
       (
SELECT id FROM airports WHERE city = 'Fiftyville')
   AND flights.year = 2023
   AND flights.month = 7
   AND flights.day = 29
 ORDER BY flights.hour, flights.minute;
