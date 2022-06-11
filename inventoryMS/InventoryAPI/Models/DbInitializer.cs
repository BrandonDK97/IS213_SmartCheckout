using Microsoft.EntityFrameworkCore;

namespace InventoryAPI.Models
{
    public class DbInitializer
    {
        private readonly ModelBuilder modelBuilder;

        public DbInitializer(ModelBuilder modelBuilder)
        {
            this.modelBuilder = modelBuilder;
        }

        public void Seed()
        {
            modelBuilder.Entity<Product>().HasData(
                new Product() { Id = 1, Name = "Bottle of Water", Description = "Evian's water is number 1", Price = 4, Quantity = 50, StoreId = 400 },
                new Product() { Id = 2, Name = "Coca-colar Zero Sugar", Description = "Diet coke helps you lose weight", Price = 1, Quantity = 50, StoreId = 300 },
                new Product() { Id = 3, Name = "Pocari Sweat Isotonic Drink", Description = "Drink this after gyms = gains", Price = 2, Quantity = 100, StoreId = 400 },
                new Product() { Id = 4, Name = "Fresh Produce Broccoli, 2 Count", Description = "Eat your veggies", Price = 3, Quantity = 20, StoreId = 400 },
                new Product() { Id = 5, Name = "Meiji Fresh Milk 2L - Chilled", Description = "Meiji milk", Price = 4, Quantity = 50, StoreId = 400 },
                new Product() { Id = 6, Name = "N&N Big Fresh Eggs, 10 x 65g", Description = "Eggs", Price = 6, Quantity = 30, StoreId = 400 },
                new Product() { Id = 7, Name = "Yakult Cultured Milk Drink Original, 5 x 100ml-chilled", Price = 10, Quantity = 30, StoreId = 200 }
            );
        }
    }
}