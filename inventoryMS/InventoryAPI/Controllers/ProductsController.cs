#nullable disable
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using InventoryAPI.Models;

namespace InventoryAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProductsController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public ProductsController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: api/Products
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Product>>> GetProducts()
        {
            return await _context.Products.ToListAsync();
        }

        // GET: api/Products/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Product>> GetProduct(int id)
        {
            var product = await _context.Products.FindAsync(id);

            if (product == null)
            {
                return StatusCode(StatusCodes.Status404NotFound, new { message = "Product not found" });
            }

            return product;
        }

        //Find product and minus quantity
        [HttpGet("{id}/{quantity}")]
        public async Task<ActionResult<Product>> GetProductMinusQuantity(int id, int quantity)
        {
            var product = await _context.Products.FindAsync(id);

            if (product == null)
            {
                return StatusCode(StatusCodes.Status404NotFound, new { message = "Product not found" });
            }

            product.Quantity = product.Quantity - quantity;

            _context.Entry(product).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!ProductExists(id))
                {
                    return StatusCode(StatusCodes.Status404NotFound, new { message = "Product not found" });
                }
                else
                {
                    throw;
                }
            }
            //return status code 200
            return StatusCode(StatusCodes.Status200OK, new { message = "Product Quantity Updated", product });
        }

        //Find product and add quantity
        [HttpGet("add/{id}/{quantity}")]
        public async Task<ActionResult<Product>> GetProductAddQuantity(int id, int quantity)
        {
            var product = await _context.Products.FindAsync(id);

            if (product == null)
            {
                return StatusCode(StatusCodes.Status404NotFound, new { message = "Product not found" });
            }

            product.Quantity = product.Quantity + quantity;

            _context.Entry(product).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!ProductExists(id))
                {
                    return StatusCode(StatusCodes.Status404NotFound, new { message = "Product not found" });
                }
                else
                {
                    throw;
                }
            }
            //return status code 200
            return StatusCode(StatusCodes.Status200OK, new { message = "Product Quantity Updated", product });
        }

        // PUT: api/Products/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutProduct(int id, Product product)
        {
            if (id != product.Id)
            {
                return BadRequest();
            }

            _context.Entry(product).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!ProductExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Products
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Product>> PostProduct(Product product)
        {
            _context.Products.Add(product);
            await _context.SaveChangesAsync();

            //return CreatedAtAction("GetProduct", new { id = product.Id }, product);
            return StatusCode(StatusCodes.Status200OK, new { message = "New Product Added to Database", product });
   
        }

        // DELETE: api/Products/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteProduct(int id)
        {
            var product = await _context.Products.FindAsync(id);
            if (product == null)
            {
                return StatusCode(StatusCodes.Status404NotFound, new { message = "Product not found" });
 
            }

            _context.Products.Remove(product);
            await _context.SaveChangesAsync();

            return StatusCode(StatusCodes.Status200OK, new { message = "Product Deleted from Database", product });
        }

        private bool ProductExists(int id)
        {
            return _context.Products.Any(e => e.Id == id);
        }
    }
}
