CREATE table strongs_dictionary (
    id serial PRIMARY Key,
    number varchar(50) not null,
    type varchar(50) not null
);
CREATE table languages (
    id serial primary key,
    title varchar(200) not null
);
CREATE table strong_values (
    id serial primary key,
    language_id integer not null,
    strongs_dictionary_id varchar(200) not null,
    CONSTRAINT languages_language_id_fkey foreign key (language_id)
        references languages (id) match simple
        on update no action on delete no action,
    CONSTRAINT strongs_dictionary_strongs_dictionary_id_fkey foreign key (strongs_dictionary_id)
        references strongs_dictionary (id) match simple
        on update no action on delete no action
);
CREATE unique index strong_index
on strongs_dictionary(number,type);

