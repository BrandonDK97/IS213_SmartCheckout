using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace InventoryAPI.Migrations
{
    public partial class SeedData : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.InsertData(
                table: "Products",
                columns: new[] { "Id", "Description", "Name", "Price", "Quantity", "StoreId" },
                values: new object[,]
                {
                    { 1, "evian is water the way nature intended.It’s a uniquely sourced mineral water that’s always naturally hydrating and refreshing, with nothing added for taste or enhanced with extras - so you can reach your natural peak.", "Evian Water 500ml", 4.0, 50, 400 },
                    { 2, "Coca-Cola is the most popular and biggest-selling soft drink in history. Created in 1886 in Atlanta it was first offered at a pharmacy by mixing Coca-Cola syrup with carbonated water. Universally loved, Coca-Cola is available in these variants: - Coca-Cola Classic - Coca-Cola Zero Sugar - Coca-Cola Light - Coca-Cola Vanilla", "Coca-cola Zero Can 320ml", 1.0, 50, 400 },
                    { 3, "A mild tasting refreshing drink which replenishes body fluids lost through perspiration.", "Pocari Sweat 1.5L", 2.0, 100, 400 },
                    { 4, "Broccoli is part of the Cabbage Family. As It Will Not Keep Long, keep Refrigerated. Country of Origin – Australia.", "Fresh Produce Broccoli, 2 Count", 3.0, 20, 400 },
                    { 5, "Meiji Pasteurized Low Fat Milk is made from 100 percent low fat fresh milk with an equivalent quality to products in Japan. It contains all the natural goodness of fresh cow’s milk. A superior taste.", "Meiji Fresh Milk 2L - Chilled", 4.0, 50, 400 },
                    { 6, "A healthier choice with Lower Cholesterol. Produced daily by N and N Agriculture Singapore (established since 2001). Big Fresh Eggs meet the stringent requirements of AVA’s Quality Egg Scheme and are 100 percent free of hormones and antibiotics.", "N&N Big Fresh Eggs, 10 x 65g", 6.0, 30, 400 },
                    { 7, "Strain Shirota was specially cultured and biotechnologically strengthened by Yakults founder Dr Minoru Shirota a microbiologist of Kyoto University in Japan in 1930 so that it can withstand the gastric juice and bile to reach the intestines alive. Thus helping to maintain a healthy digestives system. Halal Product.", "Yakult Cultured Milk Drink Original, 5 x 100ml-chilled", 10.0, 30, 400 },
                    { 8, "evian is water the way nature intended.It’s a uniquely sourced mineral water that’s always naturally hydrating and refreshing, with nothing added for taste or enhanced with extras - so you can reach your natural peak", "Evian Water 500ml", 4.0, 50, 300 },
                    { 9, "Coca-Cola is the most popular and biggest-selling soft drink in history. Created in 1886 in Atlanta it was first offered at a pharmacy by mixing Coca-Cola syrup with carbonated water. Universally loved, Coca-Cola is available in these variants: - Coca-Cola Classic - Coca-Cola Zero Sugar - Coca-Cola Light - Coca-Cola Vanilla", "Coca-cola Zero Can 320ml", 1.0, 50, 300 },
                    { 10, "A mild tasting refreshing drink which replenishes body fluids lost through perspiration.", "Pocari Sweat 1.5L", 2.0, 100, 300 },
                    { 11, "Broccoli is part of the Cabbage Family. As It Will Not Keep Long, keep Refrigerated. Country of Origin – Australia.", "Fresh Produce Broccoli, 2 Count", 3.0, 20, 300 },
                    { 12, "Meiji Pasteurized Low Fat Milk is made from 100 percent low fat fresh milk with an equivalent quality to products in Japan. It contains all the natural goodness of fresh cow’s milk. A superior taste.", "Meiji Fresh Milk 2L - Chilled", 4.0, 50, 300 },
                    { 13, "A healthier choice with Lower Cholesterol. Produced daily by N and N Agriculture Singapore (established since 2001). Big Fresh Eggs meet the stringent requirements of AVA’s Quality Egg Scheme and are 100 percent free of hormones and antibiotics.", "N&N Big Fresh Eggs, 10 x 65g", 6.0, 30, 300 },
                    { 14, "Strain Shirota was specially cultured and biotechnologically strengthened by Yakults founder Dr Minoru Shirota a microbiologist of Kyoto University in Japan in 1930 so that it can withstand the gastric juice and bile to reach the intestines alive. Thus helping to maintain a healthy digestives system. Halal Product.", "Yakult Cultured Milk Drink Original, 5 x 100ml-chilled", 10.0, 30, 300 }
                });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 1);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 2);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 3);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 4);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 5);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 6);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 7);

            migrationBuilder.DeleteData(
       table: "Products",
       keyColumn: "Id",
       keyValue: 8);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 9);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 10);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 11);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 12);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 13);

            migrationBuilder.DeleteData(
                table: "Products",
                keyColumn: "Id",
                keyValue: 14);
        }
    }
}
