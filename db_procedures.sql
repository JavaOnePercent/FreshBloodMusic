use music_db;

drop procedure if exists `track_plays_by_month`;
DELIMITER //
create procedure `track_plays_by_month` (in trc_id int, in days int)
begin
	select month(date) as month, sum(amount) as amount from api_trackplaysamount
    where trc_id_id=trc_id and date > now() - interval days day
	group by month(date)
    order by min(date);
end//
DELIMITER ;

drop procedure if exists `track_likes_by_month`;
DELIMITER //
create procedure `track_likes_by_month` (in trc_id int, in days int)
begin
	select month(date) as month, count(*) as amount from api_likedtrack 
	where trc_id_id = trc_id and date > now() - interval days day
	group by month(date)
    order by min(date);
end//
DELIMITER ;

drop procedure if exists `album_plays_by_month`;
DELIMITER //
create procedure `album_plays_by_month` (in alb_id int, in days int)
begin
	select month(date) as month, sum(amount) as amount from api_trackplaysamount
	inner join api_track on trc_id_id = api_track.id
	where alb_id_id=alb_id and date > now() - interval days day
	group by month(date)
	order by min(date);
end//
DELIMITER ;

drop procedure if exists `album_likes_by_month`;
DELIMITER //
create procedure `album_likes_by_month` (in alb_id int, in days int)
begin
	select month(date) as month, count(*) as amount from api_likedtrack
    inner join api_track on trc_id_id = api_track.id
	where alb_id_id=alb_id and date > now() - interval days day
	group by month(date)
    order by min(date);
end//
DELIMITER ;

drop procedure if exists `performer_plays_by_month`;
DELIMITER //
create procedure `performer_plays_by_month` (in per_id int, in days int)
begin
	select month(date) as month, sum(amount) as amount from api_trackplaysamount
	inner join api_track on trc_id_id = api_track.id
	inner join api_album on alb_id_id = api_album.id
	where per_id_id=per_id and date > now() - interval days day
	group by month(date)
	order by min(date);
end//
DELIMITER ;

drop procedure if exists `performer_likes_by_month`;
DELIMITER //
create procedure `performer_likes_by_month` (in per_id int, in days int)
begin
	select month(date) as month, count(*) as amount from api_likedtrack
	inner join api_track on trc_id_id = api_track.id
	inner join api_album on alb_id_id = api_album.id
	where per_id_id=per_id and date > now() - interval days day
	group by month(date)
	order by min(date);
end//
DELIMITER ;

drop procedure if exists `track_plays_by_day`;
DELIMITER //
create procedure `track_plays_by_day` (in trc_id int, in days int)
begin
	select min(date) as date, sum(amount) as amount from api_trackplaysamount
    where trc_id_id=trc_id and date > now() - interval days day
	group by date
    order by min(date);
end//
DELIMITER ;

drop procedure if exists `track_likes_by_day`;
DELIMITER //
create procedure `track_likes_by_day` (in trc_id int, in days int)
begin
	select min(date) as date, count(*) as amount from api_likedtrack 
	where trc_id_id = trc_id and date > now() - interval days day
	group by date
    order by min(date);
end//
DELIMITER ;

drop procedure if exists `album_plays_by_day`;
DELIMITER //
create procedure `album_plays_by_day` (in alb_id int, in days int)
begin
	select min(date) as date, sum(amount) as amount from api_trackplaysamount
	inner join api_track on trc_id_id = api_track.id
	where alb_id_id=alb_id and date > now() - interval days day
	group by date
	order by min(date);
end//
DELIMITER ;

drop procedure if exists `album_likes_by_day`;
DELIMITER //
create procedure `album_likes_by_day` (in alb_id int, in days int)
begin
	select min(date) as date, count(*) as amount from api_likedtrack
    inner join api_track on trc_id_id = api_track.id
	where alb_id_id=alb_id and date > now() - interval days day
	group by date
    order by min(date);
end//
DELIMITER ;

drop procedure if exists `performer_plays_by_day`;
DELIMITER //
create procedure `performer_plays_by_day` (in per_id int, in days int)
begin
	select min(date) as date, sum(amount) as amount from api_trackplaysamount
	inner join api_track on trc_id_id = api_track.id
	inner join api_album on alb_id_id = api_album.id
	where per_id_id=per_id and date > now() - interval days day
	group by date
	order by min(date);
end//
DELIMITER ;

drop procedure if exists `performer_likes_by_day`;
DELIMITER //
create procedure `performer_likes_by_day` (in per_id int, in days int)
begin
	select min(date) as date, count(*) as amount from api_likedtrack
	inner join api_track on trc_id_id = api_track.id
	inner join api_album on alb_id_id = api_album.id
	where per_id_id=per_id and date > now() - interval days day
	group by date
	order by min(date);
end//
DELIMITER ;