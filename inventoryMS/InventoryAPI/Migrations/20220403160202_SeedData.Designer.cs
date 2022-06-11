﻿// <auto-generated />
using InventoryAPI.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

#nullable disable

namespace InventoryAPI.Migrations
{
    [DbContext(typeof(ApplicationDbContext))]
    [Migration("20220403160202_SeedData")]
    partial class SeedData
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "6.0.3")
                .HasAnnotation("Relational:MaxIdentifierLength", 128);

            SqlServerModelBuilderExtensions.UseIdentityColumns(modelBuilder, 1L, 1);

            modelBuilder.Entity("InventoryAPI.Models.Product", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("Id"), 1L, 1);

                    b.Property<string>("Description")
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("Name")
                        .HasColumnType("nvarchar(max)");

                    b.Property<double>("Price")
                        .HasColumnType("float");

                    b.Property<int>("Quantity")
                        .HasColumnType("int");

                    b.Property<int>("StoreId")
                        .HasColumnType("int");

                    b.HasKey("Id");

                    b.ToTable("Products");

                    b.HasData(
                        new
                        {
                            Id = 1,
                            Description = "Evian's water is number 1",
                            Name = "Bottle of Water",
                            Price = 4.0,
                            Quantity = 50,
                            StoreId = 400
                        },
                        new
                        {
                            Id = 2,
                            Description = "Diet coke helps you lose weight",
                            Name = "Coca-colar Zero Sugar",
                            Price = 1.0,
                            Quantity = 50,
                            StoreId = 300
                        },
                        new
                        {
                            Id = 3,
                            Description = "Drink this after gyms = gains",
                            Name = "Pocari Sweat Isotonic Drink",
                            Price = 2.0,
                            Quantity = 100,
                            StoreId = 400
                        },
                        new
                        {
                            Id = 4,
                            Description = "Eat your veggies",
                            Name = "Fresh Produce Broccoli, 2 Count",
                            Price = 3.0,
                            Quantity = 20,
                            StoreId = 400
                        },
                        new
                        {
                            Id = 5,
                            Description = "Meiji milk",
                            Name = "Meiji Fresh Milk 2L - Chilled",
                            Price = 4.0,
                            Quantity = 50,
                            StoreId = 400
                        },
                        new
                        {
                            Id = 6,
                            Description = "Eggs",
                            Name = "N&N Big Fresh Eggs, 10 x 65g",
                            Price = 6.0,
                            Quantity = 30,
                            StoreId = 400
                        },
                        new
                        {
                            Id = 7,
                            Name = "Yakult Cultured Milk Drink Original, 5 x 100ml-chilled",
                            Price = 10.0,
                            Quantity = 30,
                            StoreId = 200
                        });
                });
#pragma warning restore 612, 618
        }
    }
}
