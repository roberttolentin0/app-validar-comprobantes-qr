PGDMP                      |            db_validaciones    16.1    16.1                 0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    57793    db_validaciones    DATABASE     �   CREATE DATABASE db_validaciones WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Peru.1252';
    DROP DATABASE db_validaciones;
                postgres    false            �            1259    57811    comprobantes    TABLE     U  CREATE TABLE public.comprobantes (
    id integer NOT NULL,
    ruc character(11) NOT NULL,
    fecha_emision date NOT NULL,
    serie character varying(8) NOT NULL,
    numero character varying(15) NOT NULL,
    monto double precision NOT NULL,
    updated_at date,
    created_at date NOT NULL,
    id_tipo_comprobante integer NOT NULL
);
     DROP TABLE public.comprobantes;
       public         heap    postgres    false            �            1259    57810    comprobantes_id_seq    SEQUENCE     �   CREATE SEQUENCE public.comprobantes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.comprobantes_id_seq;
       public          postgres    false    218                       0    0    comprobantes_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.comprobantes_id_seq OWNED BY public.comprobantes.id;
          public          postgres    false    217            �            1259    57825    estado_comprobante    TABLE     (  CREATE TABLE public.estado_comprobante (
    id integer NOT NULL,
    estado_comprobante integer,
    estado_ruc character varying(2),
    cod_domiciliaria_ruc character varying(2),
    observaciones text,
    updated_at date,
    created_at date NOT NULL,
    id_comprobante integer NOT NULL
);
 &   DROP TABLE public.estado_comprobante;
       public         heap    postgres    false            �            1259    57824    estado_comprobante_id_seq    SEQUENCE     �   CREATE SEQUENCE public.estado_comprobante_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.estado_comprobante_id_seq;
       public          postgres    false    220                       0    0    estado_comprobante_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.estado_comprobante_id_seq OWNED BY public.estado_comprobante.id;
          public          postgres    false    219            �            1259    57802    tipo_comprobante    TABLE     �   CREATE TABLE public.tipo_comprobante (
    id integer NOT NULL,
    cod_comprobante character(2) NOT NULL,
    descripcion character varying(45)
);
 $   DROP TABLE public.tipo_comprobante;
       public         heap    postgres    false            �            1259    57801    tipo_comprobante_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tipo_comprobante_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.tipo_comprobante_id_seq;
       public          postgres    false    216                       0    0    tipo_comprobante_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.tipo_comprobante_id_seq OWNED BY public.tipo_comprobante.id;
          public          postgres    false    215            �            1259    57879    view_comprobantes_con_estados    VIEW       CREATE VIEW public.view_comprobantes_con_estados AS
 SELECT c.id,
    c.ruc,
    c.fecha_emision,
    c.serie,
    c.numero,
    c.monto,
    ( SELECT tp.descripcion AS tipo_comprobante
           FROM public.tipo_comprobante tp
          WHERE (tp.id = c.id_tipo_comprobante)) AS tipo_comprobante,
    ec.estado_comprobante,
    ec.estado_ruc,
    ec.cod_domiciliaria_ruc,
    ec.observaciones
   FROM (public.comprobantes c
     LEFT JOIN public.estado_comprobante ec ON ((c.id = ec.id_comprobante)))
  ORDER BY c.id DESC;
 0   DROP VIEW public.view_comprobantes_con_estados;
       public          postgres    false    220    220    216    218    218    220    218    220    218    220    218    216    218    218            �            1259    57869    view_comprobantes_sin_estados    VIEW     ~  CREATE VIEW public.view_comprobantes_sin_estados AS
 SELECT c.id,
    c.ruc,
    c.fecha_emision,
    c.serie,
    c.numero,
    c.monto,
    c.updated_at,
    c.created_at,
    c.id_tipo_comprobante
   FROM (public.comprobantes c
     LEFT JOIN public.estado_comprobante ec ON ((c.id = ec.id_comprobante)))
  WHERE ((ec.id_comprobante IS NULL) OR (ec.estado_comprobante IS NULL));
 0   DROP VIEW public.view_comprobantes_sin_estados;
       public          postgres    false    218    220    220    218    218    218    218    218    218    218    218            �            1259    57840    view_estado_comprobantes    VIEW     �  CREATE VIEW public.view_estado_comprobantes AS
 SELECT c.id,
    c.ruc,
    c.fecha_emision,
    c.serie,
    c.numero,
    c.monto,
    ( SELECT tp.descripcion AS tipo_comprobante
           FROM public.tipo_comprobante tp
          WHERE (tp.id = c.id_tipo_comprobante)) AS tipo_comprobante,
    ec.estado_comprobante,
    ec.estado_ruc,
    ec.cod_domiciliaria_ruc,
    ec.observaciones
   FROM public.comprobantes c,
    public.estado_comprobante ec
  WHERE (c.id = ec.id_comprobante)
  ORDER BY c.id DESC;
 +   DROP VIEW public.view_estado_comprobantes;
       public          postgres    false    218    216    216    220    220    220    220    220    218    218    218    218    218    218            g           2604    57814    comprobantes id    DEFAULT     r   ALTER TABLE ONLY public.comprobantes ALTER COLUMN id SET DEFAULT nextval('public.comprobantes_id_seq'::regclass);
 >   ALTER TABLE public.comprobantes ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    218    218            h           2604    57828    estado_comprobante id    DEFAULT     ~   ALTER TABLE ONLY public.estado_comprobante ALTER COLUMN id SET DEFAULT nextval('public.estado_comprobante_id_seq'::regclass);
 D   ALTER TABLE public.estado_comprobante ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    220    220            f           2604    57805    tipo_comprobante id    DEFAULT     z   ALTER TABLE ONLY public.tipo_comprobante ALTER COLUMN id SET DEFAULT nextval('public.tipo_comprobante_id_seq'::regclass);
 B   ALTER TABLE public.tipo_comprobante ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216            
          0    57811    comprobantes 
   TABLE DATA           �   COPY public.comprobantes (id, ruc, fecha_emision, serie, numero, monto, updated_at, created_at, id_tipo_comprobante) FROM stdin;
    public          postgres    false    218   ,-                 0    57825    estado_comprobante 
   TABLE DATA           �   COPY public.estado_comprobante (id, estado_comprobante, estado_ruc, cod_domiciliaria_ruc, observaciones, updated_at, created_at, id_comprobante) FROM stdin;
    public          postgres    false    220   |-                 0    57802    tipo_comprobante 
   TABLE DATA           L   COPY public.tipo_comprobante (id, cod_comprobante, descripcion) FROM stdin;
    public          postgres    false    216   �-                  0    0    comprobantes_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.comprobantes_id_seq', 1, true);
          public          postgres    false    217                       0    0    estado_comprobante_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.estado_comprobante_id_seq', 1, true);
          public          postgres    false    219                       0    0    tipo_comprobante_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.tipo_comprobante_id_seq', 2, true);
          public          postgres    false    215            n           2606    57816    comprobantes comprobantes_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.comprobantes
    ADD CONSTRAINT comprobantes_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.comprobantes DROP CONSTRAINT comprobantes_pkey;
       public            postgres    false    218            p           2606    57834 8   estado_comprobante estado_comprobante_id_comprobante_key 
   CONSTRAINT     }   ALTER TABLE ONLY public.estado_comprobante
    ADD CONSTRAINT estado_comprobante_id_comprobante_key UNIQUE (id_comprobante);
 b   ALTER TABLE ONLY public.estado_comprobante DROP CONSTRAINT estado_comprobante_id_comprobante_key;
       public            postgres    false    220            r           2606    57832 *   estado_comprobante estado_comprobante_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.estado_comprobante
    ADD CONSTRAINT estado_comprobante_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.estado_comprobante DROP CONSTRAINT estado_comprobante_pkey;
       public            postgres    false    220            j           2606    57809 5   tipo_comprobante tipo_comprobante_cod_comprobante_key 
   CONSTRAINT     {   ALTER TABLE ONLY public.tipo_comprobante
    ADD CONSTRAINT tipo_comprobante_cod_comprobante_key UNIQUE (cod_comprobante);
 _   ALTER TABLE ONLY public.tipo_comprobante DROP CONSTRAINT tipo_comprobante_cod_comprobante_key;
       public            postgres    false    216            l           2606    57807 &   tipo_comprobante tipo_comprobante_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.tipo_comprobante
    ADD CONSTRAINT tipo_comprobante_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.tipo_comprobante DROP CONSTRAINT tipo_comprobante_pkey;
       public            postgres    false    216            s           2606    57819 3   comprobantes comprobantes_id_tipo_comprobrante_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.comprobantes
    ADD CONSTRAINT comprobantes_id_tipo_comprobrante_fkey FOREIGN KEY (id_tipo_comprobante) REFERENCES public.tipo_comprobante(id);
 ]   ALTER TABLE ONLY public.comprobantes DROP CONSTRAINT comprobantes_id_tipo_comprobrante_fkey;
       public          postgres    false    4716    218    216            t           2606    57835 9   estado_comprobante estado_comprobante_id_comprobante_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.estado_comprobante
    ADD CONSTRAINT estado_comprobante_id_comprobante_fkey FOREIGN KEY (id_comprobante) REFERENCES public.comprobantes(id);
 c   ALTER TABLE ONLY public.estado_comprobante DROP CONSTRAINT estado_comprobante_id_comprobante_fkey;
       public          postgres    false    4718    218    220            
   @   x�3�4203�4����0��LtLu�8�<9�,,L�,8M��8c���f@%�F\1z\\\ #X         %   x�3�4�40 �?2202�50�50�4����� c-�         a   x�=�K@0�����	d���IZ���ʑ\�Fb�=�`��M���I
�š!	���_w����
Y�8/�Ѐ;���vS�S������Y�H��     