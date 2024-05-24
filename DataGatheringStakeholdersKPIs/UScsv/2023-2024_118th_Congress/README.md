# LegiScan Public Datasets

## JSON Datasets
Compared to the CSV datasets the JSON collection represents the most complete
version of LegiScan data. These files are meant to be processed by another
application, either custom written or the LegiScan API Client import utility.

	[Import Tool](https://api.legiscan.com/docs/class-LegiScan_Import.html)

## LegiScan API Client
The API Client is an open source PHP application that supports Pull, Push,
and Bulk loading into a defined database schema. For more information see
the source code and documentation links below.

	[LegiScan API Client Source](https://api.legiscan.com/dl/)
	[LegiScan API Client Documentation](https://api.legiscan.com/docs/)

## State Links
Note that state URLs are not actively maintained for historical data in past
sessions and may no longer be accessible. The LegiScan URL for each object is
a permalink that will always be valid.

## Directory Structure
Archives are structured to enable unpacking multiple files in the same location,
creating the generic structure below, where `STATE` is the state abbreviation, and
`SESSION` is the name of the session, with `bill`, `people` and `vote` sub-directories
containing the individual JSON payloads for their respective objects.

	STATE/
	STATE/SESSION/
	STATE/SESSION/bill/
	STATE/SESSION/people/
	STATE/SESSION/vote/

### bill Directory
The JSON payload from the getBill API hook; each bill stored individually as
`BILL_NUMBER.json` (e.g., `HB1.json`', `SR10.json`)

### people Directory
The JSON payload from the getPerson API hook; each person stored individually as
`PEOPLE_ID.json` (e.g., `1357.json`', `2468.json`)

### vote Directory
The JSON payload from the getRollcall API hook; each vote stored individually as
`ROLL_CALL_ID.json` (e.g., `135791.json`', `246802.json`)