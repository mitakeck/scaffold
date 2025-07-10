using Microsoft.AspNetCore.Mvc;

namespace {{namespace}}
{
    /// <summary>
    /// {{name}} Controller
    /// Author: {{author}}
    /// Created: {{date}}
    /// </summary>
    public class {{name}}Controller : Controller
    {
        /// <summary>
        /// GET: {{name}}
        /// </summary>
        public ActionResult Index()
        {
            return View();
        }

        /// <summary>
        /// GET: {{name}}/Details/5
        /// </summary>
        public ActionResult Details(int id)
        {
            return View();
        }

        /// <summary>
        /// GET: {{name}}/Create
        /// </summary>
        public ActionResult Create()
        {
            return View();
        }

        /// <summary>
        /// POST: {{name}}/Create
        /// </summary>
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create(IFormCollection collection)
        {
            try
            {
                // TODO: Add insert logic here
                return RedirectToAction(nameof(Index));
            }
            catch
            {
                return View();
            }
        }

        /// <summary>
        /// GET: {{name}}/Edit/5
        /// </summary>
        public ActionResult Edit(int id)
        {
            return View();
        }

        /// <summary>
        /// POST: {{name}}/Edit/5
        /// </summary>
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit(int id, IFormCollection collection)
        {
            try
            {
                // TODO: Add update logic here
                return RedirectToAction(nameof(Index));
            }
            catch
            {
                return View();
            }
        }

        /// <summary>
        /// GET: {{name}}/Delete/5
        /// </summary>
        public ActionResult Delete(int id)
        {
            return View();
        }

        /// <summary>
        /// POST: {{name}}/Delete/5
        /// </summary>
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Delete(int id, IFormCollection collection)
        {
            try
            {
                // TODO: Add delete logic here
                return RedirectToAction(nameof(Index));
            }
            catch
            {
                return View();
            }
        }
    }
}